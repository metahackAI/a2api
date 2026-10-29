"""Streaming OpenAPI importer producing validated, disabled Capability IR."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import re
from typing import Iterator, Mapping

from ..contracts import compile_contract, parse_json
from ..errors import A2APIError, contract_error
from ..http_adapter import (
    HTTPHeaderParameter, HTTPQueryParameter, HTTPResponse, HTTPRoute,
    HTTP_METHODS as SUPPORTED_METHODS, MANAGED_HEADERS, SENSITIVE_HEADERS, json_media_type,
)
from ..ir import Capability, freeze, thaw
from .schema_conversion import ImportIssue, SchemaConverter, escape, local_reference

HTTP_METHODS = frozenset({'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'})
MAX_DOCUMENT_BYTES = 64 * 1024 * 1024


def load_openapi(path: str | Path) -> tuple[dict, str]:
    """Load bounded JSON/YAML, optionally gzipped. Never fetch external references."""
    path = Path(path)
    try:
        opener = gzip.open if path.suffix == '.gz' else open
        with opener(path, 'rb') as stream:
            raw = stream.read(MAX_DOCUMENT_BYTES + 1)
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise ValueError('document exceeds 64 MiB')
        text = raw.decode('utf-8')
        suffix = Path(path.stem).suffix if path.suffix == '.gz' else path.suffix
        if suffix.lower() in ('.yaml', '.yml'):
            document = _load_yaml(text)
        else:
            document = parse_json(text)
        # Reject non-JSON values (including YAML object aliases/cycles and NaN).
        json.dumps(document, allow_nan=False)
    except A2APIError:
        raise
    except (OSError, EOFError, UnicodeError, ValueError, TypeError, RecursionError) as error:
        raise A2APIError('INVALID_OPENAPI', 'OpenAPI input must be bounded, unambiguous UTF-8 JSON or YAML.') from error
    return document, hashlib.sha256(raw).hexdigest()


def _load_yaml(text: str):
    try:
        import yaml
    except ModuleNotFoundError:
        raise A2APIError('DEPENDENCY_MISSING', 'YAML input requires: python -m pip install "a2api[openapi]"') from None
    try:
        if any(isinstance(event, yaml.AliasEvent) for event in yaml.parse(text)):
            raise ValueError('YAML aliases are outside this import profile')

        class Loader(yaml.SafeLoader):
            pass

        # OAS YAML must roundtrip JSON values; keep unquoted dates and "on" as strings.
        Loader.yaml_implicit_resolvers = {
            key: [(tag, expression) for tag, expression in value
                  if tag not in ('tag:yaml.org,2002:timestamp', 'tag:yaml.org,2002:bool')]
            for key, value in Loader.yaml_implicit_resolvers.items()
        }
        Loader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false|True|False|TRUE|FALSE)$'), list('tTfF'))

        def mapping(loader, node):
            result = {}
            for key, value in loader.construct_pairs(node):
                if not isinstance(key, str) or key in result:
                    raise ValueError('YAML mapping keys must be unique strings')
                result[key] = value
            return result

        Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
        return yaml.load(text, Loader=Loader)
    except yaml.YAMLError as error:
        raise ValueError('Invalid YAML') from error


@dataclass(frozen=True)
class ImportRecord:
    path: str
    method: str
    operation_id: str
    status: str
    diagnostics: tuple[Mapping, ...]
    capability: Capability | None = None
    binding: Mapping | None = None

    def summary(self) -> dict:
        return {'path': self.path, 'method': self.method, 'operationId': self.operation_id,
                'status': self.status, 'capabilityId': self.capability.id if self.capability else None,
                'diagnostics': thaw(self.diagnostics)}

    def http_route(self, base_url: str, *, path_prefix: str = '', headers: dict | None = None, credential_provider=None) -> HTTPRoute:
        """Make a binding only after the host explicitly chooses the origin.

        This does not review or activate the disabled capability.
        """
        if self.binding is None:
            raise contract_error('No imported HTTP binding exists')
        if path_prefix and not path_prefix.startswith('/'):
            raise contract_error('Deployment path prefix must be origin-relative')
        query = {name: HTTPQueryParameter(item['pointer'], item['required'], item['explode'])
                 for name, item in self.binding['queryParameters'].items()}
        body = self.binding.get('requestBody') or {}
        responses = {int(status): HTTPResponse(item['mediaType']) for status, item in self.binding['responses'].items()}
        return HTTPRoute(base_url, path_prefix.rstrip('/') + self.path,
                         self.binding['pathParameters'], headers or {}, query, 'result',
                         method=self.method.upper(), request_body_pointer=body.get('pointer'),
                         request_body_required=body.get('required', False), request_media_type=body.get('mediaType', 'application/json'),
                         responses=responses, response_status_field=self.binding.get('responseStatusField'),
                         header_parameters={name: HTTPHeaderParameter(**item) for name, item in self.binding.get('headerParameters', {}).items()},
                         credential_provider=credential_provider)


def _object(properties: dict, required: list | None = None) -> dict:
    return {'type': 'object', 'properties': properties, 'required': required or [], 'additionalProperties': False}


def _identifier(namespace: str, operation_id: str) -> str:
    parts = []
    for part in re.split(r'[/.]', operation_id.casefold()):
        part = re.sub(r'[^a-z0-9_]', '_', part).strip('_') or 'operation'
        parts.append(part if part[0].isalpha() else 'op_' + part)
    return namespace + '.' + '.'.join(parts)


class OpenAPIImporter:
    def __init__(self, document: dict, *, namespace: str = 'imported', source_name: str = '<memory>', source_hash: str | None = None,
                 methods: set[str] | None = None):
        if not isinstance(document, dict) or not isinstance(document.get('openapi'), str) or not re.fullmatch(r'3\.[01]\.\d+', document['openapi']):
            raise A2APIError('INVALID_OPENAPI', 'Only OpenAPI 3.0.x and 3.1.x documents are supported.')
        if not isinstance(document.get('info'), dict) or not isinstance(document['info'].get('title'), str) or not isinstance(document['info'].get('version'), str):
            raise A2APIError('INVALID_OPENAPI', 'OpenAPI info.title and info.version must be strings.')
        if not isinstance(document.get('paths'), dict):
            raise A2APIError('INVALID_OPENAPI', 'OpenAPI paths must be an object.')
        if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*', namespace):
            raise A2APIError('INVALID_OPENAPI', 'Namespace must contain lowercase identifier segments.')
        dialect = document.get('jsonSchemaDialect')
        if dialect not in (None, 'https://json-schema.org/draft/2020-12/schema', 'https://spec.openapis.org/oas/3.1/dialect/base'):
            raise A2APIError('INVALID_OPENAPI', 'Custom JSON Schema dialects require a separate importer.')
        try:
            canonical = json.dumps(document, ensure_ascii=False, sort_keys=True, allow_nan=False)
        except (ValueError, TypeError, RecursionError):
            raise A2APIError('INVALID_OPENAPI', 'OpenAPI source must contain finite JSON values.') from None
        # Detach from caller mutations; component conversion caches are per document.
        self.document = json.loads(canonical)
        self.namespace = namespace
        self.source_name = source_name
        self.source_hash = source_hash or hashlib.sha256(canonical.encode()).hexdigest()
        if methods is not None and (isinstance(methods, str) or not methods or
                any(not isinstance(method, str) or method.upper() not in SUPPORTED_METHODS for method in methods)):
            raise A2APIError('INVALID_SELECTION', 'Select one or more supported HTTP methods.')
        self.methods = frozenset(method.upper() for method in methods) if methods is not None else frozenset({'GET'})
        self.converter = SchemaConverter(self.document)
        self.request_converter = SchemaConverter(self.document, direction='request')
        self._operations = list(self._inventory())
        self._ids = Counter(opid for _, _, _, _, opid, _ in self._operations)
        self._capability_ids = Counter(_identifier(namespace, opid) for _, _, _, _, opid, _ in self._operations)

    @classmethod
    def from_file(cls, path: str | Path, *, namespace: str = 'imported', methods: set[str] | None = None) -> OpenAPIImporter:
        document, digest = load_openapi(path)
        return cls(document, namespace=namespace, source_name=Path(path).name, source_hash=digest, methods=methods)

    def _object(self, value, location: str) -> dict:
        visited = set()
        while isinstance(value, dict) and '$ref' in value:
            reference = value['$ref']
            if not isinstance(reference, str):
                raise ImportIssue('INVALID_REFERENCE', 'Reference must be a string.', location)
            if reference in visited:
                raise ImportIssue('CYCLIC_OBJECT_REFERENCE', 'Reference Objects cannot form a cycle.', location)
            visited.add(reference)
            if set(value) - {'$ref', 'summary', 'description'}:
                raise ImportIssue('REFERENCE_OBJECT_SIBLINGS', 'Reference Object siblings are unsupported in this position.', location)
            value = local_reference(self.document, reference, location)
        if not isinstance(value, dict):
            raise ImportIssue('INVALID_OBJECT', 'Expected an OpenAPI object.', location)
        return value

    def _inventory(self):
        for path, raw in sorted(self.document['paths'].items()):
            if path.startswith('x-'):
                continue
            if not path.startswith('/'):
                raise A2APIError('INVALID_OPENAPI', 'Path keys must start with /.')
            location = '/paths/' + escape(path)
            try:
                item = self._object(raw, location)
            except ImportIssue as error:
                yield path, '*', {}, {}, 'unresolved-path-item', error
                continue
            for method in sorted(HTTP_METHODS & item.keys()):
                operation = item[method]
                issue = None
                if not isinstance(operation, dict):
                    operation = {}
                    issue = ImportIssue('INVALID_OPERATION', 'HTTP operation must be an object.', location + '/' + method)
                opid = operation.get('operationId')
                if opid is not None and (not isinstance(opid, str) or not opid):
                    issue = ImportIssue('INVALID_OPERATION_ID', 'operationId must be a nonempty string.', location + '/' + method)
                    opid = None
                opid = opid or method + '_' + hashlib.sha256(path.encode()).hexdigest()[:16]
                yield path, method, item, operation, opid, issue

    def iter_operations(self, operation_ids: set[str] | None = None) -> Iterator[ImportRecord]:
        """Stream records to bound memory on large specifications; no API calls occur."""
        if operation_ids is not None and not operation_ids.issubset(self._ids):
            raise A2APIError('INVALID_SELECTION', 'Selected operationId is absent from the source document.')
        for path, method, item, operation, opid, initial_issue in self._operations:
            if operation_ids is not None and opid not in operation_ids:
                continue
            location = '/paths/' + escape(path) + '/' + method
            try:
                if initial_issue:
                    raise initial_issue
                if self._ids[opid] > 1:
                    raise ImportIssue('DUPLICATE_OPERATION_ID', 'operationId is not unique in this document.', location)
                if method.upper() not in self.methods:
                    issue = ImportIssue('METHOD_NOT_SELECTED', 'Method was not selected for import; the operation remains in the inventory.', location)
                    yield ImportRecord(path, method, opid, 'skipped', (freeze(issue.diagnostic('info')),))
                    continue
                yield self._import(path, method, item, operation, opid, location)
            except ImportIssue as error:
                yield ImportRecord(path, method, opid, 'unsupported', (freeze(error.diagnostic()),))

    def _parameter_types(self, schema, location: str, depth: int = 0) -> set[str]:
        if depth > 128:
            raise ImportIssue('SCHEMA_DEPTH', 'Parameter schema exceeds the supported structural depth.', location)
        visited = set()
        while isinstance(schema, dict) and '$ref' in schema:
            reference = schema['$ref']
            if not isinstance(reference, str):
                raise ImportIssue('INVALID_REFERENCE', 'Reference must be a string.', location)
            if reference in visited:
                raise ImportIssue('UNSUPPORTED_PARAMETER_SCHEMA', 'Recursive parameter schema cannot be serialized.', location)
            visited.add(reference)
            schema = local_reference(self.document, reference, location)
        if not isinstance(schema, dict):
            raise ImportIssue('UNSUPPORTED_PARAMETER_SCHEMA', 'Parameter must declare scalar or scalar-array types.', location)
        if schema.get('nullable') is True:
            raise ImportIssue('UNSUPPORTED_PARAMETER_SCHEMA', 'Nullable parameter serialization is not defined by this profile.', location)
        declared = schema.get('type')
        if declared is not None and not (isinstance(declared, str) or
                isinstance(declared, list) and all(isinstance(value, str) for value in declared)):
            raise ImportIssue('INVALID_SCHEMA', 'Parameter type must be a string or an array of strings.', location)
        types = {declared} if isinstance(declared, str) else set(declared or [])
        if not types and ('anyOf' in schema or 'oneOf' in schema):
            alternatives = schema.get('anyOf', schema.get('oneOf', []))
            if not isinstance(alternatives, list):
                raise ImportIssue('INVALID_SCHEMA', 'Parameter alternatives must be an array.', location)
            for branch in alternatives:
                types.update(self._parameter_types(branch, location, depth + 1))
            if not types:
                raise ImportIssue('UNSUPPORTED_PARAMETER_SCHEMA', 'Parameter alternatives must declare serializable types.', location)
            return types
        if not types or types - {'string', 'integer', 'number', 'boolean', 'array'}:
            raise ImportIssue('UNSUPPORTED_PARAMETER_SCHEMA', 'Only scalar or scalar-array parameters are serialized.', location)
        if 'array' in types:
            if self._parameter_types(schema.get('items'), location + '/items', depth + 1) - {'string', 'integer', 'number', 'boolean'}:
                raise ImportIssue('UNSUPPORTED_PARAMETER_SCHEMA', 'Array items must be scalar values.', location)
        return types

    def _parameters(self, item: dict, operation: dict, location: str):
        parameters = {}
        for parent, source_location in ((item, location.rsplit('/', 1)[0]), (operation, location)):
            raw_parameters = parent.get('parameters', [])
            if not isinstance(raw_parameters, list):
                raise ImportIssue('INVALID_PARAMETERS', 'parameters must be an array.', source_location)
            seen = set()
            for index, raw in enumerate(raw_parameters):
                pointer = source_location + '/parameters/' + str(index)
                parameter = self._object(raw, pointer)
                name, where = parameter.get('name'), parameter.get('in')
                if not isinstance(name, str) or not name or where not in ('path', 'query', 'header', 'cookie'):
                    raise ImportIssue('INVALID_PARAMETER', 'Parameter must have a name and supported OpenAPI location.', pointer)
                key = (where, name.lower() if where == 'header' else name)
                if key in seen:
                    raise ImportIssue('DUPLICATE_PARAMETER', 'Parameter name/location appears twice at the same level.', pointer)
                seen.add(key)
                parameters[key] = (parameter, pointer)
        return parameters

    def _responses(self, method: str, operation: dict, location: str):
        responses = operation.get('responses')
        if not isinstance(responses, dict):
            raise ImportIssue('NO_SUPPORTED_SUCCESS', 'Explicit success response declarations are required.', location + '/responses')
        if any(re.fullmatch(r'2[xX]{2}', code) for code in responses):
            raise ImportIssue('UNSUPPORTED_SUCCESS_RANGE', 'Success status ranges require explicit per-status codecs.', location + '/responses')
        success = {int(code): value for code, value in responses.items() if re.fullmatch(r'2\d\d', code)}
        if not success:
            raise ImportIssue('NO_SUPPORTED_SUCCESS', 'At least one explicit 2xx response is required.', location + '/responses')
        schemas, details, diagnostics = {}, {}, []
        for status, raw in sorted(success.items()):
            pointer = location + '/responses/' + str(status)
            response = self._object(raw, pointer)
            content = response.get('content', {})
            if not isinstance(content, dict):
                raise ImportIssue('UNSUPPORTED_RESPONSE', 'Response content must be an object.', pointer)
            if method == 'head' or not content:
                schema, media = {'type': 'null'}, None
            else:
                if status in (204, 205):
                    raise ImportIssue('UNSUPPORTED_RESPONSE', '204/205 responses cannot declare content.', pointer)
                media = sorted((name for name in content if json_media_type(name)), key=lambda name: (name != 'application/json', name))
                if not media or not isinstance(content[media[0]], dict) or 'schema' not in content[media[0]]:
                    raise ImportIssue('UNSUPPORTED_RESPONSE', 'Success response requires a JSON schema or an explicitly empty body.', pointer)
                media = media[0]
                schema, warnings = self.converter.convert(content[media]['schema'], pointer + '/content/' + escape(media) + '/schema')
                diagnostics.extend(warnings)
            schemas[status] = schema
            details[str(status)] = {'mediaType': media, 'links': response.get('links', {})}
        return schemas, details, diagnostics

    def _import(self, path: str, method: str, item: dict, operation: dict, opid: str, location: str) -> ImportRecord:
        if 'requestBody' in operation and method in {'get', 'head'}:
            raise ImportIssue('GET_REQUEST_BODY', 'GET/HEAD request bodies are outside this import profile.', location + '/requestBody')
        diagnostics = []
        schemas = {'path': {}, 'query': {}, 'headers': {}}
        required = {'path': [], 'query': [], 'headers': []}
        path_bindings, query_bindings, header_bindings = {}, {}, {}
        input_roots = []
        for (where, name), (parameter, pointer) in self._parameters(item, operation, location).items():
            if where == 'header':
                if name in SENSITIVE_HEADERS or name in MANAGED_HEADERS:
                    raise ImportIssue('UNSUPPORTED_HEADER_PARAMETER', 'Credential and managed HTTP headers must be provided by the host.', pointer)
                where = 'headers'
            if where not in schemas:
                raise ImportIssue('UNSUPPORTED_PARAMETER_LOCATION', 'Cookie parameters require a separate serialization profile.', pointer)
            if 'schema' not in parameter or 'content' in parameter:
                raise ImportIssue('UNSUPPORTED_PARAMETER_CONTENT', 'Parameter must use a schema, not content serialization.', pointer)
            if type(parameter.get('required', False)) is not bool:
                raise ImportIssue('INVALID_PARAMETER', 'Parameter required must be a boolean.', pointer)
            if where == 'path' and parameter.get('required') is not True:
                raise ImportIssue('INVALID_PATH_PARAMETER', 'Path parameters must be required.', pointer)
            types = self._parameter_types(parameter['schema'], pointer + '/schema')
            if where == 'path' and ('array' in types or parameter.get('style', 'simple') != 'simple' or parameter.get('explode', False)):
                raise ImportIssue('UNSUPPORTED_PATH_SERIALIZATION', 'Path serialization supports simple scalar values only.', pointer)
            if where == 'query' and (parameter.get('style', 'form') != 'form' or parameter.get('allowReserved', False)):
                raise ImportIssue('UNSUPPORTED_QUERY_SERIALIZATION', 'Query serialization supports form with reserved characters encoded.', pointer)
            if where == 'headers' and ('array' in types or parameter.get('style', 'simple') != 'simple'):
                raise ImportIssue('UNSUPPORTED_HEADER_SERIALIZATION', 'Header serialization supports simple scalar values only.', pointer)
            if type(parameter.get('explode', where == 'query')) is not bool:
                raise ImportIssue('INVALID_PARAMETER', 'Parameter explode must be boolean.', pointer)
            converted, warnings = self.request_converter.convert(parameter['schema'], pointer + '/schema')
            if 'description' in parameter:
                if not isinstance(parameter['description'], str):
                    raise ImportIssue('INVALID_PARAMETER', 'Parameter description must be a string.', pointer)
                converted = dict(converted)
                converted.setdefault('description', parameter['description'])
            if 'example' in parameter:
                converted = dict(converted)
                converted.setdefault('examples', [parameter['example']])
            diagnostics.extend(warnings)
            schemas[where][name] = converted
            input_roots.append(converted)
            if parameter.get('required', False):
                required[where].append(name)
            source_pointer = '/' + where + '/' + escape(name)
            if where == 'path':
                path_bindings[name] = source_pointer
            elif where == 'headers':
                header_bindings[name] = {'pointer': source_pointer, 'required': parameter.get('required', False)}
            else:
                query_bindings[name] = {'pointer': source_pointer, 'required': parameter.get('required', False),
                                        'explode': parameter.get('explode', True)}
        placeholders = set(re.findall(r'\{([^{}]+)\}', path))
        if placeholders != set(path_bindings):
            raise ImportIssue('PATH_PARAMETER_MISMATCH', 'Template placeholders and path parameter declarations differ.', location)
        input_properties = {where: _object(properties, required[where]) for where, properties in schemas.items() if properties}
        input_required = [where for where in input_properties if required[where]]
        body_binding = None
        if 'requestBody' in operation:
            pointer = location + '/requestBody'
            body = self._object(operation['requestBody'], pointer)
            if type(body.get('required', False)) is not bool:
                raise ImportIssue('INVALID_REQUEST_BODY', 'Request body required must be boolean.', pointer)
            content = body.get('content', {})
            if not isinstance(content, dict):
                raise ImportIssue('INVALID_REQUEST_BODY', 'Request content must be an object.', pointer)
            media = sorted((name for name in content if json_media_type(name)), key=lambda name: (name != 'application/json', name))
            if not media or not isinstance(content[media[0]], dict) or 'schema' not in content[media[0]] or content[media[0]].get('encoding'):
                raise ImportIssue('UNSUPPORTED_REQUEST_BODY', 'Request bodies require a JSON schema without custom encoding.', pointer)
            body_schema, warnings = self.request_converter.convert(content[media[0]]['schema'], pointer + '/content/' + escape(media[0]) + '/schema')
            diagnostics.extend(warnings)
            input_properties['body'] = body_schema
            input_roots.append(body_schema)
            if body.get('required', False):
                input_required.append('body')
            body_binding = {'pointer': '/body', 'required': body.get('required', False), 'mediaType': media[0]}
        result_schemas, response_details, warnings = self._responses(method, operation, location)
        diagnostics.extend(warnings)
        input_definitions, warnings, input_refs = self.request_converter.bundle(input_roots)
        diagnostics.extend(warnings)
        definitions, warnings, source_refs = self.converter.bundle(list(result_schemas.values()))
        diagnostics.extend(warnings)
        input_schema = _object(input_properties, input_required)
        result_schema = next(iter(result_schemas.values())) if len(result_schemas) == 1 else {'anyOf': list(result_schemas.values())}
        output_schema = _object({'result': result_schema}, ['result'])
        status_field = None if method == 'get' and list(result_schemas) == [200] and response_details['200']['mediaType'] else 'httpStatus'
        if status_field:
            output_schema['properties'][status_field] = {'type': 'integer', 'enum': list(result_schemas)}
            output_schema['required'].append(status_field)
            if len(result_schemas) > 1:
                output_schema['allOf'] = [{'if': {'properties': {status_field: {'const': code}}},
                                          'then': {'properties': {'result': schema}}} for code, schema in result_schemas.items()]
        for schema, bundled in ((input_schema, input_definitions), (output_schema, definitions)):
            schema['$schema'] = 'https://json-schema.org/draft/2020-12/schema'
            if bundled:
                schema['$defs'] = bundled
        capability_id = _identifier(self.namespace, opid)
        if self._capability_ids[capability_id] > 1:
            capability_id += '_' + hashlib.sha256((method + ' ' + path).encode()).hexdigest()[:12]
        summary = operation.get('summary') or opid
        if not isinstance(summary, str) or not isinstance(operation.get('description', ''), str):
            raise ImportIssue('INVALID_OPERATION', 'Summary/description must be strings.', location)
        source = {'document': self.source_name, 'sha256': self.source_hash, 'openapiVersion': self.document['openapi'],
                  'apiVersion': self.document['info']['version'], 'pointer': location, 'operationId': opid,
                  'method': method.upper(), 'path': path, 'responses': response_details,
                  'security': operation.get('security', self.document.get('security', [])),
                  'servers': operation.get('servers', item.get('servers', self.document.get('servers', []))),
                  'schemaReferences': {**input_refs, **source_refs}, 'tags': operation.get('tags', [])}
        manifest = {
            'a2api': '0.1.0-draft.1', 'schemaProfile': 'openapi-draft', 'id': capability_id, 'version': '0.1.0',
            'lifecycle': 'draft', 'enabled': False, 'title': summary, 'owner': 'unassigned',
            'intent': {'summary': summary + ('\n' + operation['description'] if operation.get('description') else ''),
                       'useWhen': [summary], 'avoidWhen': ['Before business semantics, authorization and effects have been reviewed.']},
            'inputSchema': input_schema, 'outputSchema': output_schema, 'semanticTypes': {},
            'contextRequirements': ['actor', 'tenant'], 'effects': {'kind': 'unknown', 'externalWrites': True},
            'policy': {'requiredScopes': ['a2api:unreviewed'], 'objectAuthorization': 'backend_and_runtime',
                       'resourceRelationshipCheck': 'review_required', 'approval': 'review_required'},
            'operations': [{'id': opid, 'serviceRef': self.namespace, 'operationRef': opid, 'httpMethod': method.upper(),
                            'effects': {'kind': 'unknown', 'externalWrites': True},
                            'inputSchema': input_schema, 'outputSchema': output_schema}],
            'binding': {'type': 'composition', 'steps': [{'id': 'fetch', 'operationId': opid,
                        'input': {key: {'from': 'input', 'pointer': '/' + key} for key in input_properties}}],
                        'output': {key: {'from': 'step', 'step': 'fetch', 'pointer': '/' + key} for key in output_schema['properties']}},
            'execution': {'mode': 'synchronous', 'deadlineMs': 5000, 'backendTimeoutMs': 1500, 'maxBackendCalls': 1,
                          'maxRetries': 0, 'failureMode': 'stop', 'successCondition': 'all_required_steps_succeeded_and_output_valid'},
            'errors': ['INVALID_INPUT', 'SCHEMA_MISMATCH', 'PERMISSION_DENIED', 'DEADLINE_EXCEEDED', 'OUTCOME_UNKNOWN'],
            'presentation': {'view': 'json', 'pointer': '/result'},
            'examples': [{'userIntent': summary, 'expectedDecision': 'review_required'}],
            'provenance': {'kind': 'source', 'reviewState': 'unreviewed', 'source': source},
        }
        try:
            capability = compile_contract(manifest)
        except A2APIError as error:
            raise ImportIssue('IR_VALIDATION_FAILED', error.detail, location) from None
        binding = {'serviceRef': self.namespace, 'operationRef': opid, 'method': method.upper(), 'path': path,
                   'pathParameters': path_bindings, 'queryParameters': query_bindings, 'responseEnvelope': 'result',
                   'headerParameters': header_bindings, 'requestBody': body_binding, 'responseStatusField': status_field,
                   'responses': {status: {'mediaType': item['mediaType']} for status, item in response_details.items()},
                   'deploymentRequired': True}
        try:
            ImportRecord(path, method, opid, 'imported', (), capability, binding).http_route('https://deployment.invalid')
        except A2APIError as error:
            raise ImportIssue('UNSUPPORTED_HTTP_BINDING', error.detail, location) from None
        unique = {json.dumps(diagnostic, sort_keys=True): diagnostic for diagnostic in diagnostics}
        diagnostics = tuple(freeze(unique[key]) for key in sorted(unique))
        return ImportRecord(path, method, opid, 'imported', diagnostics, capability, freeze(binding))


def write_import(importer: OpenAPIImporter, output: str | Path, *, operation_ids: set[str] | None = None) -> dict:
    """Write to a new directory; existing generated or user files are never overwritten."""
    output = Path(output)
    if operation_ids is not None and not operation_ids.issubset(importer._ids):
        raise A2APIError('INVALID_SELECTION', 'Selected operationId is absent from the source document.')
    from ..openapi_dependencies import canonical_bytes, dependency_index, snapshot
    dependencies = dependency_index(importer)
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise A2APIError('OUTPUT_EXISTS', 'Choose a new output directory; existing files are not overwritten.') from None
    contracts = output / 'contracts'
    contracts.mkdir()
    records = []
    statuses, methods, diagnostic_codes = Counter(), Counter(), Counter()
    for record in importer.iter_operations(operation_ids):
        summary = record.summary()
        statuses[record.status] += 1
        methods[record.method] += 1
        diagnostic_codes.update(d['code'] for d in record.diagnostics)
        if record.capability:
            filename = record.capability.id + '.json'
            (contracts / filename).write_text(json.dumps(record.capability.describe(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            (contracts / (record.capability.id + '.http.json')).write_text(json.dumps(thaw(record.binding), indent=2) + '\n', encoding='utf-8')
            summary['contract'] = 'contracts/' + filename
        records.append(summary)
    report = {'source': importer.source_name, 'sourceSha256': importer.source_hash, 'openapi': importer.document['openapi'],
              'sourceSnapshot': 'source.snapshot.json', 'dependencyIndex': 'dependencies.json',
              'requestedMethods': sorted(importer.methods),
              'selection': sorted(operation_ids) if operation_ids is not None else None,
              'summary': {'sourceOperations': len(importer._operations), 'operations': len(records), 'statuses': dict(sorted(statuses.items())),
                          'methods': dict(sorted(methods.items())), 'diagnostics': dict(sorted(diagnostic_codes.items()))},
              'operations': records}
    (output / 'source.snapshot.json').write_bytes(canonical_bytes(snapshot(importer)))
    (output / 'dependencies.json').write_bytes(canonical_bytes(dependencies))
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report
