"""Axum Router/method handlers and a closed Serde DTO source profile.

Routes are read from literal `Router::new().route(...)` chains, including routers combined with
`.merge(...)` (paths unchanged) and `.nest("/prefix", ...)` with a literal prefix (inline or a
module's router function). Both `{param}` and the older `:param` path syntax are read. Handlers
are resolved by name within their module path. Extractors that are not Path/Query/Json (State,
Extension, headers and the project's own `FromRequest` types such as an authenticated user) are
supplied by the request context, never by the model; the import notes them.
"""

import re

from .source import SourceImporter, Unsupported, literal, named, object_schema, record, split_types, text, walk

METHODS = {'get': 'GET', 'head': 'HEAD', 'post': 'POST', 'put': 'PUT', 'patch': 'PATCH', 'delete': 'DELETE'}
STATUS = {'OK': 200, 'CREATED': 201, 'ACCEPTED': 202, 'NO_CONTENT': 204, 'RESET_CONTENT': 205, 'PARTIAL_CONTENT': 206}
SERDE_KEYS = ('rename', 'rename_all', 'default', 'skip', 'skip_serializing_if', 'skip_serializing', 'skip_deserializing',
              'flatten', 'with', 'deny_unknown_fields')
CONTEXT_EXTRACTORS = ('State', 'Extension', 'HeaderMap', 'TypedHeader', 'ConnectInfo', 'Host', 'OriginalUri',
                      'Method', 'Uri', 'Version', 'Request', 'Parts', 'CookieJar', 'Session')
STRING_SERDE = ('time::serde::rfc3339', 'time::serde::iso8601', 'chrono::serde::ts_rfc3339', 'humantime_serde')


def serde(node):
    attrs, sibling = {}, node.prev_named_sibling
    while sibling and sibling.type in ('attribute_item', 'line_comment', 'block_comment'):
        raw = text(sibling)
        if raw.startswith('#[serde('):
            content = raw[len('#[serde('):-2]
            for item in split_types(content):
                parts = item.split('=', 1)
                key = parts[0].strip()
                if key not in SERDE_KEYS:
                    raise Unsupported('Custom Serde behavior needs an explicit schema: ' + key)
                if len(parts) == 2:
                    try:attrs[key] = __import__('json').loads(parts[1].strip())
                    except ValueError:raise Unsupported('Serde metadata must be literal.') from None
                else:attrs[key] = True
        sibling = sibling.prev_named_sibling
    if 'with' in attrs and attrs['with'] not in STRING_SERDE:
        raise Unsupported('Custom Serde behavior needs an explicit schema: with')
    return attrs


def _calls_with_ancestors(root):
    """Yield (call_expression, ancestors) in source order without Node.parent."""
    pending = [(root, ())]
    while pending:
        current, ancestors = pending.pop()
        if current.type == 'call_expression':
            yield current, ancestors
        lineage = ancestors + (current,)
        pending.extend((child, lineage) for child in reversed(current.named_children))


def camel(name):
    first, *rest = name.split('_')
    return first + ''.join(part[:1].upper() + part[1:] for part in rest)


def rename(name, policy):
    if policy in (None, 'snake_case'):
        return name
    if policy == 'camelCase':
        return camel(name)
    if policy == 'PascalCase':
        return ''.join(part[:1].upper() + part[1:] for part in name.split('_'))
    if policy == 'kebab-case':
        return name.replace('_', '-')
    if policy == 'SCREAMING_SNAKE_CASE':
        return name.upper()
    if policy == 'lowercase':
        return name.lower()
    raise Unsupported('Unsupported Serde rename_all policy.')


def _module(path):
    """`src/http/articles/mod.rs` -> ('http', 'articles'); `src/http/users.rs` -> ('http', 'users')."""
    parts = [part for part in re.split(r'[\\/]', path) if part]
    stem = parts[-1].removesuffix('.rs')
    parts = parts[:-1] + ([] if stem in ('mod', 'lib', 'main') else [stem])
    return tuple(parts)


class RustSourceImporter(SourceImporter):
    language, extension = 'rust', '.rs'

    def _extract(self):
        self.models, self.functions, self.extractors, self.string_types = {}, {}, set(), {'output': set(), 'input': set()}
        for path, unit in self.units:
            for node in walk(unit):
                if node.type in ('struct_item', 'enum_item'):
                    self.models.setdefault(text(named(node, 'name')), []).append(node)
                elif node.type == 'function_item':
                    self.functions.setdefault(text(named(node, 'name')), []).append((path, node))
                elif node.type == 'impl_item' and named(node, 'trait') is not None:
                    trait = re.sub(r'<.*', '', text(named(node, 'trait'))).split('::')[-1]
                    target = re.sub(r'<.*', '', text(named(node, 'type'))).split('::')[-1]
                    body = text(named(node, 'body')) if named(node, 'body') else ''
                    if trait in ('FromRequest', 'FromRequestParts'):
                        self.extractors.add(target)
                    elif trait == 'Serialize' and re.search(r'\b(collect_str|serialize_str)\b', body):
                        self.string_types['output'].add(target)
                    elif trait == 'Deserialize' and re.search(r'\b(visit_str|deserialize_str|String::deserialize)\b', body):
                        self.string_types['input'].add(target)
        prefixes = self._nest_prefixes()
        for path, unit in self.units:
            for call, ancestors in _calls_with_ancestors(unit):
                function = named(call, 'function')
                if function.type != 'field_expression' or text(named(function, 'field')) != 'route':continue
                route = ''
                location = f'{path}:{call.start_point.row + 1}'
                try:
                    prefix, owner = '', None
                    # Ancestors come from a top-down walk: Node.parent is unreliable on deep route chains.
                    for index in range(len(ancestors) - 1, -1, -1):
                        ancestor = ancestors[index]
                        if ancestor.type == 'function_item':
                            owner = text(named(ancestor, 'name'))
                            break
                        if ancestor.type == 'call_expression':
                            caller = named(ancestor, 'function')
                            field = text(named(caller, 'field')) if caller and caller.type == 'field_expression' else ''
                            inside_arguments = index + 1 < len(ancestors) and ancestors[index + 1].type == 'arguments'
                            if field in ('nest', 'nest_service') and inside_arguments:
                                first = named(ancestor, 'arguments').named_children[0]
                                if first.type != 'string_literal':
                                    raise Unsupported('Nested routers need a literal prefix.')
                                prefix = literal(first).rstrip('/') + prefix
                    if owner is not None:
                        found = prefixes.get((_module(path), owner), [''])
                        if len(set(found)) != 1:
                            raise Unsupported('This router is nested under several prefixes; select one explicitly.')
                        prefix = found[0] + prefix
                    if 'Router::new()' not in text(named(function, 'value')):
                        raise Unsupported('Use a literal Router::new().route chain.')
                    args = named(call, 'arguments').named_children
                    route = self._path(prefix + literal(args[0]))
                    pairs = self._method_router(args[1])
                except (Unsupported, IndexError, AttributeError) as error:
                    yield self.unsupported(f'unresolved_{_module(path)[-1] if _module(path) else "root"}_{call.start_byte}',
                                           route, '', location, error)
                    continue
                for verb, handler_ref in pairs:
                    handler_name = handler_ref.split('::')[-1]
                    try:
                        handler_path, handler = self._resolve(handler_ref, path)
                        yield self._handler(handler_name, route, verb, handler, f'{handler_path}:{handler.start_point.row + 1}')
                    except (Unsupported, AttributeError, TypeError, IndexError) as error:
                        yield self.unsupported(handler_name, route, verb, location, error)

    def _nest_prefixes(self):
        """{(module, router function): [prefix]} for `.nest("/p", module::router())` calls."""
        found = {}
        for path, unit in self.units:
            for call, _ in _calls_with_ancestors(unit):
                function = named(call, 'function')
                if function.type != 'field_expression' or text(named(function, 'field')) not in ('nest', 'nest_service'):
                    continue
                args = named(call, 'arguments').named_children
                if len(args) != 2 or args[0].type != 'string_literal' or args[1].type != 'call_expression':
                    continue
                target = text(named(args[1], 'function'))
                if not re.fullmatch(r'[\w:]+', target):
                    continue
                *modules, name = target.split('::')
                module = tuple(m for m in (*_module(path), *modules) if m not in ('self', 'crate', 'super'))
                found.setdefault((module, name), []).append(literal(args[0]).rstrip('/'))
        return found

    @staticmethod
    def _path(route):
        if re.search(r'/\*', route):
            raise Unsupported('Wildcard routes need an explicit binding.')
        return re.sub(r'/:([A-Za-z_][A-Za-z0-9_]*)', r'/{\1}', route) or '/'

    def _resolve(self, reference, path):
        *modules, name = reference.split('::')
        choices = self.functions.get(name, [])
        if len(choices) > 1:
            here = [choice for choice in choices if choice[0] == path]
            wanted = [m for m in modules if m not in ('self', 'crate', 'super')]
            matched = [choice for choice in choices if wanted and _module(choice[0])[-len(wanted):] == tuple(wanted)]
            choices = matched or (here if not wanted else [])
        if len(choices) != 1:
            raise Unsupported('Missing or ambiguous Rust handler.')
        return choices[0]

    def _method_router(self, expression):
        if expression.type != 'call_expression':raise Unsupported('Use an explicit Axum method router.')
        function, args = named(expression, 'function'), named(expression, 'arguments').named_children
        if function.type == 'field_expression':
            base = self._method_router(named(function, 'value'))
            method = text(named(function, 'field'))
        else:
            base, method = [], text(function).split('::')[-1]
        if method not in METHODS or len(args) != 1 or args[0].type not in ('identifier', 'scoped_identifier'):
            raise Unsupported('Method routers require one explicit named handler.')
        return base + [(METHODS[method], text(args[0]))]

    def schema(self, typename, *, direction='output', stack=(), substitutions=None):
        substitutions = substitutions or {}
        typename = re.sub(r'\s+', ' ', typename.strip())
        typename = substitutions.get(typename, typename)
        if len(stack) > 32 or typename in stack:raise Unsupported('Recursive/deep Rust DTOs need a finite wrapper.')
        if typename == '()':
            return {'type': 'null'}
        scalars = {'String': 'string', 'str': 'string', '&str': 'string', 'bool': 'boolean', 'f32': 'number', 'f64': 'number',
                   'char': 'string'}
        if typename in scalars:return {'type': scalars[typename]}
        if re.fullmatch('[iu](8|16|32|64|128)|[iu]size', typename):
            result = {'type': 'integer'}
            if typename.startswith('u'):result['minimum'] = 0
            return result
        bare = typename.split('<', 1)[0].split('::')[-1]
        if bare in ('Uuid',):
            return {'type': 'string', 'format': 'uuid'}
        if bare == 'Value' and 'serde_json' in typename or typename == 'Value':
            return {}
        if bare in ('DateTime', 'NaiveDateTime', 'NaiveDate'):
            return {'type': 'string', 'format': 'date' if bare == 'NaiveDate' else 'date-time'} if bare != 'NaiveDateTime' else {'type': 'string'}
        if bare in self.string_types[direction]:
            return {'type': 'string'}
        match = re.fullmatch(r'([\w:]+)<(.+)>', typename)
        if match:
            name, inside = match.groups();args = split_types(inside)
            name = name.split('::')[-1]
            if name in ('Json', 'Vec', 'Option', 'Box', 'Arc', 'Rc', 'VecDeque', 'HashSet', 'BTreeSet') and len(args) == 1:
                child = self.schema(args[0], direction=direction, stack=stack, substitutions=substitutions)
                if name in ('Vec', 'VecDeque', 'HashSet', 'BTreeSet'):return {'type': 'array', 'items': child}
                if name == 'Option':return {'anyOf': [child, {'type': 'null'}]}
                return child
            if name in ('HashMap', 'BTreeMap') and len(args) == 2 and args[0] in ('String', '&str'):
                return {'type': 'object', 'additionalProperties': self.schema(args[1], direction=direction, stack=stack,
                                                                              substitutions=substitutions)}
            if name == 'Result' and len(args) in (1, 2):
                return self.schema(args[0], direction=direction, stack=stack, substitutions=substitutions)
        else:
            name, args = typename.split('::')[-1], []
        choices = self.models.get(name, [])
        if len(choices) != 1:raise Unsupported('Unresolved/ambiguous Rust DTO: ' + typename)
        model = choices[0];attrs = serde(model)
        policy = attrs.get('rename_all')
        parameters = named(model, 'type_parameters')
        variables = []
        for parameter in parameters.named_children if parameters else ():
            if parameter.type == 'lifetime' or parameter.type == 'lifetime_parameter':
                continue
            pieces = text(parameter).split('=', 1)
            variables.append((pieces[0].split(':')[0].strip(), pieces[1].strip() if len(pieces) == 2 else None))
        if len(args) > len(variables) or any(default is None for _, default in variables[len(args):]):
            raise Unsupported('Generic DTO needs concrete type arguments: ' + typename)
        local = {**substitutions}
        for index, (variable, default) in enumerate(variables):
            local[variable] = args[index] if index < len(args) else substitutions.get(default, default)
        if model.type == 'enum_item':
            variants = [c for c in named(model, 'body').named_children if c.type == 'enum_variant']
            if any(named(v, 'body') is not None for v in variants) or attrs.keys() - {'rename_all'}:
                raise Unsupported('Data-carrying or tagged Serde enums need an explicit schema.')
            return {'type': 'string', 'enum': [serde(v).get('rename', rename(text(named(v, 'name')), policy)) for v in variants]}
        body = named(model, 'body')
        if body is not None and body.type == 'ordered_field_declaration_list':
            fields = [c for c in body.named_children if c.type not in ('attribute_item', 'visibility_modifier', 'line_comment')]
            if len(fields) == 1:  # newtype struct: serialized as its one field
                return self.schema(text(fields[0]), direction=direction, stack=stack + (typename,), substitutions=local)
        if body is None or body.type != 'field_declaration_list':raise Unsupported('Use a named-field Serde struct.')
        props, required = {}, []
        for field in body.named_children:
            if field.type != 'field_declaration':continue
            meta = serde(field)
            if 'skip' in meta or ('skip_serializing' if direction == 'output' else 'skip_deserializing') in meta:continue
            if meta.get('skip_serializing_if') not in (None, 'Option::is_none', 'Vec::is_empty', 'String::is_empty'):
                raise Unsupported('Unsupported conditional Serde serialization.')
            original, kind = text(named(field, 'name')), text(named(field, 'type'))
            if 'flatten' in meta:
                inner = self.schema(kind, direction=direction, stack=stack + (typename,), substitutions=local)
                if inner.get('type') != 'object' or set(inner['properties']) & set(props):
                    raise Unsupported('Flattened Serde fields need a struct with distinct names.')
                props.update(inner['properties']);required.extend(inner['required'])
                continue
            key = meta.get('rename', rename(original, policy))
            if key in props:raise Unsupported('Duplicate Serde field name.')
            props[key] = ({'type': 'string', 'format': 'date-time'} if meta.get('with') in STRING_SERDE
                          else self.schema(kind, direction=direction, stack=stack + (typename,), substitutions=local))
            optional = (kind.startswith('Option<') or 'default' in meta or 'default' in attrs) if direction == 'input' else 'skip_serializing_if' in meta
            if not optional:required.append(key)
        return object_schema(props, required)

    def _handler(self, opid, route, verb, handler, location):
        groups, required, paths, queries, has_body = {}, [], {}, {}, False
        placeholders = re.findall(r'\{([^{}]+)\}', route)
        context = []
        for param in named(handler, 'parameters').named_children:
            if param.type in ('line_comment', 'block_comment', 'attribute_item'):
                continue
            if param.type != 'parameter':raise Unsupported('Only explicit Axum extractor parameters are supported.')
            typename = re.sub(r'\s+', ' ', text(named(param, 'type')))
            match = re.fullmatch(r'(?:axum::)?(?:extract::)?(Path|Query|Json|State|Extension|Form)<(.+)>', typename)
            bare = typename.split('<', 1)[0].split('::')[-1]
            if not match:
                if bare in CONTEXT_EXTRACTORS or bare in self.extractors or bare == 'Option' and re.sub(
                        r'^Option<(.+)>$', r'\1', typename).split('<')[0].split('::')[-1] in self.extractors:
                    context.append(bare)
                    continue
                raise Unsupported('Unsupported Axum extractor: ' + typename)
            kind, inner = match.groups()
            if kind in ('State', 'Extension'):continue
            if kind == 'Form':raise Unsupported('Form bodies are outside the JSON profile.')
            if kind == 'Path':
                if inner.startswith('('):
                    types = split_types(inner[1:-1])
                    if len(types) != len(placeholders):raise Unsupported('Path tuple arity does not match placeholders.')
                    schema = object_schema({key: self.schema(t, direction='input') for key, t in zip(placeholders, types)}, placeholders)
                elif len(placeholders) == 1 and inner in ('String', 'u64', 'i64', 'u32', 'i32', 'usize', 'Uuid'):
                    schema = object_schema({placeholders[0]: self.schema(inner, direction='input')}, placeholders)
                else:schema = self.schema(inner, direction='input')
                if schema.get('type') != 'object':raise Unsupported('Path extractor must bind named scalar fields.')
                groups['path'] = schema;required.append('path')
                paths.update({key: '/path/' + key for key in schema['properties']})
            elif kind == 'Query':
                schema = self.schema(inner, direction='input')
                if schema.get('type') != 'object':raise Unsupported('Query extractor needs a struct.')
                schema = {**schema, 'properties': {key: (item['anyOf'][0] if 'anyOf' in item and len(item['anyOf']) == 2
                                                         and item['anyOf'][1] == {'type': 'null'} else item)
                                                   for key, item in schema['properties'].items()}}
                groups['query'] = schema
                if schema['required']:required.append('query')
                queries.update({key: {'pointer': '/query/' + key, 'required': key in schema['required'], 'explode': True} for key in schema['properties']})
            elif kind == 'Json':
                if has_body:raise Unsupported('Only one JSON extractor is supported.')
                groups['body'] = self.schema(inner, direction='input');required.append('body');has_body = True
        if context:
            self.warn('CONTEXT_EXTRACTOR', 'Supplied by the request context, not the caller: ' + ', '.join(sorted(set(context))) + '.')
        returned = re.sub(r'\s+', ' ', text(named(handler, 'return_type')) if named(handler, 'return_type') else '()')
        wrapped = re.fullmatch(r'(?:[\w:]+::)?Result<(.+)>', returned)
        if wrapped:
            # Result<(StatusCode, Json<T>), StatusCode>: errors are status-only; Ok carries the declared status.
            arms = split_types(wrapped[1])
            if len(arms) == 2 and arms[0].startswith('(StatusCode,') and arms[1] == 'StatusCode':
                returned = arms[0]
            elif len(arms) in (1, 2):
                returned = arms[0]
        body = named(handler, 'body')
        tail = body.named_children[-1] if body.named_children else body
        codes = ({STATUS[text(node).split('::')[-1]] for node in walk(tail, 'scoped_identifier')
                  if text(node).startswith('StatusCode::') and text(node).split('::')[-1] in STATUS}
                 if returned == 'StatusCode' or returned.startswith('(StatusCode,') else set())
        if len(codes) > 1:raise Unsupported('Multiple success statuses require an explicit contract.')
        status = next(iter(codes), 200)
        if returned == 'StatusCode':
            if not codes or status not in (204, 205) and verb != 'HEAD':raise Unsupported('Empty response requires an explicit 204/205 status or HEAD.')
            output = {'type': 'null'}
        elif returned.startswith('(StatusCode,'):
            parts = split_types(returned[1:-1])
            if len(parts) != 2 or not codes:raise Unsupported('Tuple response requires one explicit status and JSON body.')
            output = self.schema(parts[1])
        elif returned == '()':
            output = {'type': 'null'}
        elif returned.startswith('impl '):
            output = self.open_output(f'`{returned}` does not name the response body type')
        else:
            try:
                output = self.schema(returned)
            except Unsupported as error:
                output = self.open_output(str(error))
        return record(self.namespace, opid, route, verb, object_schema(groups, required), output, location,
                      statuses=(status,), path_bindings=paths, query_bindings=queries, body=has_body)
