"""Go net/http ServeMux, named handlers and explicit encoding/json DTOs."""

import re

from .source import SourceImporter, Unsupported, literal, named, object_schema, record, text, walk


STATUS = {'StatusOK': 200, 'StatusCreated': 201, 'StatusAccepted': 202, 'StatusNoContent': 204,
          'StatusResetContent': 205, 'StatusPartialContent': 206}


class GoSourceImporter(SourceImporter):
    language, extension = 'go', '.go'

    def _extract(self):
        self.models, self.functions = {}, {}
        for path, unit in self.units:
            for node in walk(unit, 'type_spec'):
                self.models.setdefault(text(named(node, 'name')), []).append(named(node, 'type'))
            for node in walk(unit, 'function_declaration'):
                self.functions.setdefault(text(named(node, 'name')), []).append((path, node))
        for path, unit in self.units:
            muxes = set()
            for node in walk(unit, 'short_var_declaration'):
                if text(named(node, 'right')) == 'http.NewServeMux()':
                    muxes.add(text(named(node, 'left')))
            for call in walk(unit, 'call_expression'):
                function = named(call, 'function')
                if function.type != 'selector_expression' or text(named(function, 'field')) != 'HandleFunc':
                    continue
                opid, route, verb = 'unresolved_' + str(call.start_byte), '', ''
                location = f'{path}:{call.start_point.row + 1}'
                try:
                    receiver = text(named(function, 'operand'))
                    if receiver not in muxes | {'http'}:
                        raise Unsupported('Only http.HandleFunc or a local http.NewServeMux variable is supported.')
                    args = named(call, 'arguments').named_children
                    if len(args) != 2 or args[1].type != 'identifier':
                        raise Unsupported('Register a named handler and literal METHOD path.')
                    opid = text(args[1])
                    pattern = literal(args[0])
                    if ' ' not in pattern:
                        raise Unsupported('ServeMux registration must include an explicit HTTP method.')
                    verb, route = pattern.split(' ', 1)
                    choices = self.functions.get(opid, [])
                    if len(choices) != 1:
                        raise Unsupported('Handler is missing or ambiguous.')
                    handler_path, handler = choices[0]
                    yield self._handler(opid, route, verb, handler, f'{handler_path}:{handler.start_point.row + 1}')
                except (Unsupported, AttributeError, TypeError) as error:
                    yield self.unsupported(opid, route, verb, location, str(error) or 'Unsupported route syntax.')

    def schema(self, typename, stack=(), *, direction='input'):
        typename = typename.strip()
        if len(stack) > 32 or typename in stack:
            raise Unsupported('Recursive/deep Go structs require a finite wrapper.')
        if typename.startswith('*'):
            return {'anyOf': [self.schema(typename[1:], stack, direction=direction), {'type': 'null'}]}
        if typename.startswith('[]'):
            if typename[2:] in ('byte', 'uint8'):
                raise Unsupported('Go byte slices use a base64 JSON codec; an explicit schema is required.')
            return {'anyOf': [{'type': 'array', 'items': self.schema(typename[2:], stack, direction=direction)}, {'type': 'null'}]}
        array = re.fullmatch(r'\[(\d+)\](.+)', typename)
        if array:
            return {'type': 'array', 'items': self.schema(array[2], stack, direction=direction), 'minItems': int(array[1]), 'maxItems': int(array[1])}
        scalars = {'string': 'string', 'bool': 'boolean', 'int': 'integer', 'int8': 'integer', 'int16': 'integer',
                   'int32': 'integer', 'int64': 'integer', 'uint': 'integer', 'uint8': 'integer', 'uint16': 'integer',
                   'uint32': 'integer', 'uint64': 'integer', 'float32': 'number', 'float64': 'number'}
        if typename in scalars:
            item = {'type': scalars[typename]}
            if typename.startswith('uint'):item['minimum'] = 0
            return item
        choices = self.models.get(typename, [])
        if len(choices) != 1:
            raise Unsupported('Unresolved/ambiguous Go JSON type: ' + typename)
        model = choices[0]
        for _, unit in self.units:
            for method in walk(unit, 'method_declaration'):
                if text(named(method, 'name')) in ('MarshalJSON', 'UnmarshalJSON', 'MarshalText', 'UnmarshalText'):
                    receiver = text(named(method, 'receiver'))
                    if re.search(r'\b' + re.escape(typename) + r'\b', receiver):
                        raise Unsupported('Custom Go JSON methods need an explicit schema.')
        if model.type != 'struct_type':
            return self.schema(text(model), stack + (typename,), direction=direction)
        props, required = {}, []
        fields = next(c for c in model.named_children if c.type == 'field_declaration_list')
        for field in fields.named_children:
            names = field.children_by_field_name('name')
            if not names:
                raise Unsupported('Embedded Go structs require explicit JSON fields.')
            tag = text(named(field, 'tag'))
            match = re.search(r'json:"([^"\\]*)"', tag)
            parts = match[1].split(',') if match else ['']
            if parts[0] == '-':continue
            if set(parts[1:]) - {'omitempty', 'omitzero'}:
                raise Unsupported('Custom Go JSON field codecs need an explicit schema.')
            for name in names:
                original = text(name)
                if not original[0].isupper():continue
                key = parts[0] or original
                if key in props:raise Unsupported('Duplicate JSON field name.')
                props[key] = self.schema(text(named(field, 'type')), stack + (typename,), direction=direction)
                if direction == 'output' and not set(parts[1:]) & {'omitempty', 'omitzero'}:
                    required.append(key)
        # Go decoding permits omitted fields and initializes zero values.
        return object_schema(props, required)

    def _handler(self, opid, route, verb, handler, location):
        params = named(handler, 'parameters').named_children
        if len(params) != 2 or [text(named(p, 'type')) for p in params] != ['http.ResponseWriter', '*http.Request']:
            raise Unsupported('Use an explicit net/http ResponseWriter, *Request handler signature.')
        writer = text(named(params[0], 'name')); request = text(named(params[1], 'name'))
        body = named(handler, 'body')
        variables = {}
        for node in walk(body, 'var_spec'):
            if named(node, 'type'):
                for name in node.children_by_field_name('name'):
                    variables[text(name)] = text(named(node, 'type'))
        for node in walk(body, 'short_var_declaration'):
            left, right = named(node, 'left'), named(node, 'right')
            if len(left.named_children) == len(right.named_children) == 1 and right.named_children[0].type == 'composite_literal':
                variables[text(left.named_children[0])] = text(named(right.named_children[0], 'type'))
        groups, paths, queries, output_types, statuses = {}, {}, {}, set(), set()
        has_body = False
        for call in walk(body, 'call_expression'):
            function = named(call, 'function')
            if function.type != 'selector_expression':continue
            method, operand = text(named(function, 'field')), text(named(function, 'operand'))
            args = named(call, 'arguments').named_children
            if method == 'PathValue' and operand == request:
                key = literal(args[0]);paths[key] = '/path/' + key
                group = groups.setdefault('path', object_schema({}))
                group['properties'][key] = {'type': 'string'};group['required'].append(key)
            elif method == 'Get' and operand == request + '.URL.Query()':
                key = literal(args[0]);group = groups.setdefault('query', object_schema({}))
                group['properties'][key] = {'type': 'string'}
                queries[key] = {'pointer': '/query/' + key, 'required': False, 'explode': False}
            elif method == 'Decode' and operand == f'json.NewDecoder({request}.Body)':
                if has_body or len(args) != 1:raise Unsupported('Only one explicit JSON body decoder is supported.')
                name = text(args[0]).removeprefix('&')
                if name not in variables:raise Unsupported('JSON Decode target needs a declared local type.')
                groups['body'] = self.schema(variables[name]);has_body = True
            elif method in ('Decode', 'Unmarshal'):
                raise Unsupported('Indirect/custom decoding requires a direct typed JSON decoder or explicit wrapper.')
            elif method == 'Encode' and operand == f'json.NewEncoder({writer})':
                if len(args) != 1:raise Unsupported('JSON Encode requires one statically typed value.')
                arg = args[0]
                typename = text(named(arg, 'type')) if arg.type == 'composite_literal' else variables.get(text(arg))
                if not typename:raise Unsupported('JSON Encode result needs a concrete local DTO type.')
                output_types.add(typename)
            elif method == 'WriteHeader' and operand == writer:
                raw = text(args[0]);status = int(raw) if raw.isdigit() else STATUS.get(raw.split('.')[-1])
                if status is not None and 200 <= status <= 299:statuses.add(status)
                elif not raw.startswith('http.Status') and not raw.isdigit():
                    raise Unsupported('Dynamic HTTP status is unsupported.')
        if any(text(node) == request + '.Body' for node in walk(body, 'selector_expression')) and not has_body:
            raise Unsupported('Request body use needs an explicit typed JSON decoder.')
        query_calls = [n for n in walk(body, 'call_expression') if text(named(n, 'function')) == request + '.URL.Query']
        if len(query_calls) > len(queries):
            raise Unsupported('Indirect query decoding requires explicit direct query reads.')
        if len(output_types) > 1 or len(statuses) > 1:
            raise Unsupported('Multiple success body types/statuses need an explicit response contract.')
        statuses = tuple(statuses) or (200,)
        if output_types:
            output = self.schema(output_types.pop(), direction='output')
        elif verb == 'HEAD' or statuses[0] in (204, 205):
            output = {'type': 'null'}
        else:
            raise Unsupported('No explicit typed JSON response found in the handler.')
        required = ['path'] if paths else []
        if has_body:required.append('body')
        return record(self.namespace, opid, route, verb, object_schema(groups, required), output, location,
                      path_bindings=paths, query_bindings=queries, body=has_body, statuses=statuses)
