"""Axum Router/method handlers and a closed Serde DTO source profile."""

import re

from .source import SourceImporter, Unsupported, literal, named, object_schema, record, split_types, text, walk

METHODS = {'get': 'GET', 'head': 'HEAD', 'post': 'POST', 'put': 'PUT', 'patch': 'PATCH', 'delete': 'DELETE'}
STATUS = {'OK': 200, 'CREATED': 201, 'ACCEPTED': 202, 'NO_CONTENT': 204, 'RESET_CONTENT': 205, 'PARTIAL_CONTENT': 206}


def serde(node):
    attrs, sibling = {}, node.prev_named_sibling
    while sibling and sibling.type in ('attribute_item', 'line_comment', 'block_comment'):
        raw = text(sibling)
        if raw.startswith('#[serde('):
            content = raw[len('#[serde('):-2]
            for item in split_types(content):
                parts = item.split('=', 1)
                key = parts[0].strip()
                if key not in ('rename', 'rename_all', 'default', 'skip', 'skip_serializing_if'):
                    raise Unsupported('Custom Serde behavior needs an explicit schema: ' + key)
                if len(parts) == 2:
                    try:attrs[key] = __import__('json').loads(parts[1].strip())
                    except ValueError:raise Unsupported('Serde metadata must be literal.') from None
                else:attrs[key] = True
        sibling = sibling.prev_named_sibling
    return attrs


def camel(name):
    first, *rest = name.split('_')
    return first + ''.join(part[:1].upper() + part[1:] for part in rest)


class RustSourceImporter(SourceImporter):
    language, extension = 'rust', '.rs'

    def _extract(self):
        self.models, self.functions = {}, {}
        for path, unit in self.units:
            for node in walk(unit, 'struct_item'):
                self.models.setdefault(text(named(node, 'name')), []).append(node)
            for node in walk(unit, 'function_item'):
                self.functions.setdefault(text(named(node, 'name')), []).append((path, node))
        for path, unit in self.units:
            for call in walk(unit, 'call_expression'):
                function = named(call, 'function')
                if function.type != 'field_expression' or text(named(function, 'field')) != 'route':continue
                route = ''
                location = f'{path}:{call.start_point.row + 1}'
                try:
                    ancestor = call.parent
                    while ancestor and ancestor.type != 'function_item':
                        if ancestor.type == 'call_expression':
                            owner = named(ancestor, 'function')
                            if owner and owner.type == 'field_expression' and text(named(owner, 'field')) in ('nest', 'nest_service', 'merge'):
                                raise Unsupported('Nested/merged routers need explicit resolved route prefixes.')
                        ancestor = ancestor.parent
                    if 'Router::new()' not in text(named(function, 'value')):
                        raise Unsupported('Use a literal Router::new().route chain.')
                    args = named(call, 'arguments').named_children
                    route = literal(args[0])
                    pairs = self._method_router(args[1])
                except (Unsupported, IndexError, AttributeError) as error:
                    yield self.unsupported('unresolved_' + str(call.start_byte), route, '', location, error)
                    continue
                for verb, handler_name in pairs:
                    try:
                        choices = self.functions.get(handler_name, [])
                        if len(choices) != 1:raise Unsupported('Missing or ambiguous Rust handler.')
                        handler_path, handler = choices[0]
                        yield self._handler(handler_name, route, verb, handler, f'{handler_path}:{handler.start_point.row + 1}')
                    except (Unsupported, AttributeError, TypeError) as error:
                        yield self.unsupported(handler_name, route, verb, location, error)

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
        return base + [(METHODS[method], text(args[0]).split('::')[-1])]

    def schema(self, typename, *, direction='output', stack=()):
        typename = typename.strip()
        if len(stack) > 32 or typename in stack:raise Unsupported('Recursive/deep Rust DTOs need a finite wrapper.')
        scalars = {'String': 'string', 'str': 'string', 'bool': 'boolean', 'f32': 'number', 'f64': 'number'}
        if typename in scalars:return {'type': scalars[typename]}
        if re.fullmatch('[iu](8|16|32|64)|[iu]size', typename):
            result = {'type': 'integer'}
            if typename.startswith('u'):result['minimum'] = 0
            return result
        match = re.fullmatch(r'([\w:]+)<(.+)>', typename)
        if match:
            name, inside = match.groups();args = split_types(inside)
            if name in ('Json', 'Vec', 'Option') and len(args) == 1:
                child = self.schema(args[0], direction=direction, stack=stack)
                if name == 'Vec':return {'type': 'array', 'items': child}
                if name == 'Option':return {'anyOf': [child, {'type': 'null'}]}
                return child
            if name == 'Result' and len(args) == 2:
                return self.schema(args[0], direction=direction, stack=stack)
            raise Unsupported('Unsupported generic/custom Rust type: ' + typename)
        choices = self.models.get(typename, [])
        if len(choices) != 1:raise Unsupported('Unresolved/ambiguous Rust DTO: ' + typename)
        model = choices[0];attrs = serde(model)
        if attrs.get('rename_all') not in (None, 'camelCase', 'snake_case'):
            raise Unsupported('Unsupported Serde rename_all policy.')
        body = named(model, 'body')
        if body is None or body.type != 'field_declaration_list':raise Unsupported('Use a named-field Serde struct.')
        props, required = {}, []
        for field in body.named_children:
            if field.type != 'field_declaration':continue
            meta = serde(field)
            if 'skip' in meta:continue
            if meta.get('skip_serializing_if') not in (None, 'Option::is_none'):
                raise Unsupported('Unsupported conditional Serde serialization.')
            original, kind = text(named(field, 'name')), text(named(field, 'type'))
            key = meta.get('rename', camel(original) if attrs.get('rename_all') == 'camelCase' else original)
            if key in props:raise Unsupported('Duplicate Serde field name.')
            props[key] = self.schema(kind, direction=direction, stack=stack + (typename,))
            optional = (kind.startswith('Option<') or 'default' in meta or 'default' in attrs) if direction == 'input' else 'skip_serializing_if' in meta
            if not optional:required.append(key)
        return object_schema(props, required)

    def _handler(self, opid, route, verb, handler, location):
        groups, required, paths, queries, has_body = {}, [], {}, {}, False
        placeholders = re.findall(r'\{([^{}]+)\}', route)
        for param in named(handler, 'parameters').named_children:
            if param.type != 'parameter':raise Unsupported('Only explicit Axum extractor parameters are supported.')
            typename = text(named(param, 'type'))
            match = re.fullmatch(r'(Path|Query|Json|State)<(.+)>', typename)
            if not match:raise Unsupported('Unsupported Axum extractor: ' + typename)
            kind, inner = match.groups()
            if kind == 'State':continue
            if kind == 'Path':
                if inner.startswith('('):
                    types = split_types(inner[1:-1])
                    if len(types) != len(placeholders):raise Unsupported('Path tuple arity does not match placeholders.')
                    schema = object_schema({key: self.schema(t, direction='input') for key, t in zip(placeholders, types)}, placeholders)
                elif len(placeholders) == 1 and inner in ('String', 'u64', 'i64', 'u32', 'i32'):
                    schema = object_schema({placeholders[0]: self.schema(inner, direction='input')}, placeholders)
                else:schema = self.schema(inner, direction='input')
                if schema.get('type') != 'object':raise Unsupported('Path extractor must bind named scalar fields.')
                groups['path'] = schema;required.append('path')
                paths.update({key: '/path/' + key for key in schema['properties']})
            elif kind == 'Query':
                schema = self.schema(inner, direction='input')
                if schema.get('type') != 'object':raise Unsupported('Query extractor needs a struct.')
                groups['query'] = schema
                if schema['required']:required.append('query')
                queries.update({key: {'pointer': '/query/' + key, 'required': key in schema['required'], 'explode': True} for key in schema['properties']})
            elif kind == 'Json':
                if has_body:raise Unsupported('Only one JSON extractor is supported.')
                groups['body'] = self.schema(inner, direction='input');required.append('body');has_body = True
        returned = text(named(handler, 'return_type'))
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
        else:output = self.schema(returned)
        return record(self.namespace, opid, route, verb, object_schema(groups, required), output, location,
                      statuses=(status,), path_bindings=paths, query_bindings=queries, body=has_body)
