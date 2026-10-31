"""Gin routes and gin.Context handlers, read statically for the Go importer.

Route prefixes follow `Group("/p")` through local variables and through router parameters of
registration functions (`articles.Register(v1.Group("/articles"))`), across packages. Handlers are
`func(c *gin.Context)` functions. Inputs come only from direct reads: `c.Param`, `c.Query`/
`DefaultQuery`/`GetQuery`/`QueryArray`, `ShouldBind*`/`Bind*` into a typed value, or a method of a
typed value that passes its receiver to a binder (a validator's `Bind(c)`). Outputs come from
`c.JSON(<2xx status>, value)` with a typed value or a `gin.H{...}` whose values have readable types.
"""

from __future__ import annotations

import re

from .source import Unsupported, literal, named, object_schema, record, text, walk

VERBS = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD'}
ROUTER_TYPES = ('*gin.RouterGroup', '*gin.Engine', 'gin.IRouter', 'gin.IRoutes', 'gin.RouterGroup')
JSON_WRITERS = ('JSON', 'IndentedJSON', 'PureJSON', 'SecureJSON', 'AsciiJSON')
BODY_BINDERS = ('ShouldBindJSON', 'BindJSON', 'ShouldBind', 'Bind', 'ShouldBindWith', 'BindWith', 'ShouldBindBodyWith',
                'MustBindWith')
QUERY_BINDERS = ('ShouldBindQuery', 'BindQuery')
STATUS = {'StatusOK': 200, 'StatusCreated': 201, 'StatusAccepted': 202, 'StatusNoContent': 204,
          'StatusResetContent': 205, 'StatusPartialContent': 206}


def _package(path):
    parts = re.split(r'[\\/]', path)
    return parts[-2] if len(parts) > 1 else ''


def _params(function):
    """[(name, type)] of a function's parameters."""
    found = []
    for declaration in named(function, 'parameters').named_children:
        if declaration.type not in ('parameter_declaration', 'variadic_parameter_declaration'):
            continue
        kind = text(named(declaration, 'type'))
        names = declaration.children_by_field_name('name') or [None]
        found.extend((text(name) if name is not None else None, kind) for name in names)
    return found


def _results(function):
    result = named(function, 'result')
    if result is None:
        return []
    if result.type == 'parameter_list':
        types = []
        for declaration in result.named_children:
            names = declaration.children_by_field_name('name') or [None]
            types.extend(text(named(declaration, 'type')) for _ in names)
        return types
    return [text(result)]


def _join(prefix, path):
    joined = re.sub(r'/+', '/', '/' + prefix.strip('/') + '/' + path.strip('/')).rstrip('/') or '/'
    if re.search(r'/\*', joined):
        raise Unsupported('Wildcard Gin routes need an explicit binding.')
    return re.sub(r'/:([A-Za-z_][A-Za-z0-9_]*)', r'/{\1}', joined)


class GinReader:
    def __init__(self, importer):
        self.im = importer
        self.functions, self.methods = {}, {}
        for path, unit in importer.units:
            for node in walk(unit, 'function_declaration'):
                self.functions.setdefault(text(named(node, 'name')), []).append((path, node))
            for node in walk(unit, 'method_declaration'):
                receiver_type = text(named(named(node, 'receiver').named_children[0], 'type')).lstrip('*')
                self.methods.setdefault((receiver_type, text(named(node, 'name'))), []).append((path, node))

    def uses_gin(self):
        return any('github.com/gin-gonic/gin' in text(unit) for _, unit in self.im.units)

    def function(self, reference, here):
        """A function by `name` or `pkg.name`, preferring the referenced package or the caller's."""
        package, _, name = reference.rpartition('.')
        choices = self.functions.get(name, [])
        if len(choices) > 1:
            wanted = package or _package(here)
            choices = [c for c in choices if _package(c[0]) == wanted] or ([c for c in choices if c[0] == here] if not package else [])
        return choices[0] if len(choices) == 1 else (None, None)

    # --- routes -----------------------------------------------------------------------------------

    def _groups(self, function, path, inbound):
        """{variable: {prefix}} inside one function, from its router parameters and local Group calls."""
        groups = {name: set(prefixes) for name, prefixes in inbound.items()}
        body = named(function, 'body')
        for node in walk(body) if body else ():
            if node.type not in ('short_var_declaration', 'assignment_statement', 'var_spec'):
                continue
            left = named(node, 'left') if node.type != 'var_spec' else None
            right = named(node, 'right') if node.type != 'var_spec' else named(node, 'value')
            targets = left.named_children if left is not None else node.children_by_field_name('name')
            values = right.named_children if right is not None else []
            if len(targets) != 1 or len(values) != 1:
                continue
            found = self._prefixes(values[0], groups)
            if found is not None:
                groups.setdefault(text(targets[0]), set()).update(found)
        return groups

    def _prefixes(self, expression, groups):
        raw = text(expression)
        if raw in ('gin.Default()', 'gin.New()'):
            return {''}
        if expression.type == 'identifier':
            return groups.get(raw)
        if expression.type == 'call_expression':
            function = named(expression, 'function')
            if function.type == 'selector_expression' and text(named(function, 'field')) == 'Group':
                base = self._prefixes(named(function, 'operand'), groups)
                args = named(expression, 'arguments').named_children
                if base is None or not args or args[0].type not in ('interpreted_string_literal', 'raw_string_literal'):
                    return None
                return {prefix.rstrip('/') + '/' + literal(args[0]).strip('/') for prefix in base}
        return None

    def routes(self):
        inbound = {}  # (path, function name) -> {param: {prefix}}
        for _ in range(12):
            changed = False
            for path, unit in self.im.units:
                for function in walk(unit, 'function_declaration'):
                    key = (path, text(named(function, 'name')))
                    groups = self._groups(function, path, inbound.get(key, {}))
                    for call in walk(named(function, 'body')) if named(function, 'body') else ():
                        if call.type != 'call_expression':
                            continue
                        target_path, target = self.function(text(named(call, 'function')), path)
                        if target is None:
                            continue
                        params, args = _params(target), named(call, 'arguments').named_children
                        for (name, kind), arg in zip(params, args):
                            if kind not in ROUTER_TYPES or name is None:
                                continue
                            found = self._prefixes(arg, groups)
                            if not found:
                                continue
                            slot = inbound.setdefault((target_path, text(named(target, 'name'))), {}).setdefault(name, set())
                            if not found <= slot:
                                slot.update(found)
                                changed = True
            if not changed:
                break
        seen = set()
        for path, unit in self.im.units:
            for function in walk(unit, 'function_declaration'):
                groups = self._groups(function, path, inbound.get((path, text(named(function, 'name'))), {}))
                for call in walk(named(function, 'body')) if named(function, 'body') else ():
                    if call.type != 'call_expression' or named(call, 'function').type != 'selector_expression':
                        continue
                    selector = named(call, 'function')
                    verb, args = text(named(selector, 'field')), named(call, 'arguments').named_children
                    if verb == 'Handle' and args and args[0].type == 'interpreted_string_literal':
                        verb, args = literal(args[0]), args[1:]
                    if verb not in VERBS or len(args) < 2:
                        continue
                    prefixes = self._prefixes(named(selector, 'operand'), groups)
                    if not prefixes:
                        continue
                    location = f'{path}:{call.start_point.row + 1}'
                    handler = args[-1]
                    for prefix in sorted(prefixes):
                        route = ''
                        try:
                            if args[0].type not in ('interpreted_string_literal', 'raw_string_literal'):
                                raise Unsupported('Gin routes need a literal path.')
                            route = _join(prefix, literal(args[0]))
                            if handler.type not in ('identifier', 'selector_expression'):
                                raise Unsupported('Register a named Gin handler function.')
                            key = (verb, route, text(handler))
                            if key in seen:
                                continue  # "" and "/" register the same route twice
                            seen.add(key)
                            handler_path, node = self.function(text(handler), path)
                            if node is None:
                                raise Unsupported('Gin handler is missing or ambiguous.')
                            yield self.handler(text(handler).split('.')[-1], route, verb, node, handler_path)
                        except (Unsupported, AttributeError, TypeError, IndexError) as error:
                            opid = (text(handler).split('.')[-1] if handler.type in ('identifier', 'selector_expression')
                                    else f'inline_{_package(path) or "main"}_{call.start_point.row + 1}')
                            yield self.im.unsupported(opid, route, verb, location, str(error))

    # --- handlers ---------------------------------------------------------------------------------

    def _types(self, function, path):
        """Local variable types: declarations, composite literals and (multi-)results of known functions."""
        types = {name: kind for name, kind in _params(function) if name}
        body = named(function, 'body')
        for node in walk(body) if body else ():
            if node.type == 'var_spec' and named(node, 'type') is not None:
                for name in node.children_by_field_name('name'):
                    types[text(name)] = text(named(node, 'type'))
            elif node.type == 'short_var_declaration':
                targets = named(node, 'left').named_children
                values = named(node, 'right').named_children
                if len(values) == 1 and len(targets) > 1 and values[0].type == 'call_expression':
                    results = self._call_results(values[0], types, path)
                    if results and len(results) == len(targets):
                        types.update((text(t), r) for t, r in zip(targets, results) if text(t) != '_')
                elif len(values) == len(targets):
                    for target, value in zip(targets, values):
                        kind = self.type_of(value, types, path)
                        if kind:
                            types[text(target)] = kind
        return types

    def _call_results(self, call, types, path):
        function = named(call, 'function')
        if function.type == 'selector_expression':
            operand = named(function, 'operand')
            owner = types.get(text(operand)) if operand.type == 'identifier' else None
            if owner:
                found = self.methods.get((owner.lstrip('*').split('.')[-1], text(named(function, 'field'))), [])
                return _results(found[0][1]) if len(found) == 1 else None
        target_path, target = self.function(text(function), path)
        return _results(target) if target is not None else None

    def type_of(self, node, types, path):
        if node.type == 'unary_expression' and text(node).startswith('&'):
            return self.type_of(node.named_children[0], types, path)
        if node.type == 'composite_literal':
            return text(named(node, 'type'))
        if node.type == 'identifier':
            return types.get(text(node))
        if node.type in ('interpreted_string_literal', 'raw_string_literal'):
            return 'string'
        if node.type == 'int_literal':
            return 'int'
        if node.type in ('true', 'false'):
            return 'bool'
        if node.type == 'call_expression':
            results = self._call_results(node, types, path)
            return results[0] if results else None
        return None

    def _binds_receiver(self, method):
        receiver = text(named(named(method, 'receiver').named_children[0], 'name'))
        for call in walk(named(method, 'body')):
            if call.type != 'call_expression' or 'Bind' not in text(named(call, 'function')).split('.')[-1]:
                continue
            if any(text(arg).lstrip('&') == receiver for arg in named(call, 'arguments').named_children):
                return True
        return False

    def handler(self, opid, route, verb, function, path):
        location = f'{path}:{function.start_point.row + 1}'
        params = _params(function)
        if len(params) != 1 or params[0][1] != '*gin.Context':
            raise Unsupported('Gin handlers need one *gin.Context parameter.')
        context = params[0][0]
        types = self._types(function, path)
        placeholders = re.findall(r'\{([^{}]+)\}', route)
        groups, required, paths, queries, has_body = {}, [], {}, {}, False
        if placeholders:
            groups['path'] = object_schema({name: {'type': 'string'} for name in placeholders}, placeholders)
            paths = {name: '/path/' + name for name in placeholders}
            required.append('path')
        outputs, statuses = [], set()
        im = self.im
        for call in walk(named(function, 'body')):
            if call.type != 'call_expression' or named(call, 'function').type != 'selector_expression':
                continue
            selector = named(call, 'function')
            name, operand = text(named(selector, 'field')), named(selector, 'operand')
            args = named(call, 'arguments').named_children
            if text(operand) == context:
                if name == 'Param':
                    if literal(args[0]) not in placeholders:
                        raise Unsupported('c.Param reads a name that is not in the route.')
                elif name in ('Query', 'DefaultQuery', 'GetQuery', 'QueryArray', 'GetQueryArray'):
                    key = literal(args[0])
                    item = {'type': 'array', 'items': {'type': 'string'}} if 'Array' in name else {'type': 'string'}
                    if name == 'DefaultQuery' and len(args) == 2 and args[1].type == 'interpreted_string_literal':
                        item['default'] = literal(args[1])
                    groups.setdefault('query', object_schema({}))['properties'][key] = item
                    queries[key] = {'pointer': '/query/' + key, 'required': False, 'explode': True}
                elif name in BODY_BINDERS or name in QUERY_BINDERS:
                    target = self.type_of(args[0], types, path) if args else None
                    if not target:
                        raise Unsupported(f'{name} target needs a declared type.')
                    if name in QUERY_BINDERS:
                        schema = im.schema(target, tag='form')
                        group = groups.setdefault('query', object_schema({}))
                        for key, item in schema['properties'].items():
                            if 'anyOf' in item:
                                item = item['anyOf'][0]
                            group['properties'][key] = item
                            queries[key] = {'pointer': '/query/' + key, 'required': key in schema['required'], 'explode': True}
                        group['required'].extend(schema['required'])
                    else:
                        if has_body:
                            raise Unsupported('Only one bound request body is supported.')
                        groups['body'] = im.schema(target, binding=True);has_body = True
                elif name in JSON_WRITERS and len(args) == 2:
                    raw = text(args[0]).split('.')[-1]
                    status = int(raw) if raw.isdigit() else STATUS.get(raw)
                    if status is None:
                        if raw.startswith('Status') or raw.isdigit():
                            continue  # an error status
                        raise Unsupported('Dynamic HTTP status is unsupported.')
                    statuses.add(status)
                    outputs.append(self._output(args[1], types, path))
                elif name in ('Status', 'AbortWithStatus') and args:
                    raw = text(args[0]).split('.')[-1]
                    status = int(raw) if raw.isdigit() else STATUS.get(raw)
                    if status in (204, 205):
                        statuses.add(status);outputs.append({'type': 'null'})
                elif name in ('GetRawData', 'ShouldBindUri', 'BindUri', 'FormFile', 'MultipartForm', 'PostForm'):
                    raise Unsupported(f'c.{name} input needs an explicit binding.')
            elif name in ('Bind', 'BindJSON', 'Validate') and operand.type == 'identifier' and any(
                    text(arg) == context for arg in args):
                owner = types.get(text(operand), '').lstrip('*').split('.')[-1]
                found = self.methods.get((owner, name), [])
                if len(found) == 1 and self._binds_receiver(found[0][1]):
                    if has_body:
                        raise Unsupported('Only one bound request body is supported.')
                    groups['body'] = im.schema(owner, binding=True);has_body = True
        if any(text(node) in (context + '.Request.Body', context + '.Request.Form') for node in walk(named(function, 'body'))) and not has_body:
            raise Unsupported('Request body use needs a typed Gin binding.')
        if has_body:
            required.append('body')
        if len(statuses) > 1 or any(output != outputs[0] for output in outputs):
            output = im.open_output('Several success responses need an explicit contract')
            statuses = {200, 201, 202} if not statuses & {204, 205} else statuses
        elif not outputs:
            output = im.open_output('No c.JSON success response with a readable type')
            statuses = {200, 201, 202}
        else:
            output = outputs[0] if outputs[0] is not None else im.open_output('The c.JSON value type is not readable')
        return record(im.namespace, opid, route, verb, object_schema(groups, required), output, location,
                      path_bindings=paths, query_bindings=queries, body=has_body, statuses=tuple(sorted(statuses)) or (200,))

    def _output(self, node, types, path):
        if node.type == 'composite_literal' and re.sub(r'\s', '', text(named(node, 'type'))) in (
                'gin.H', 'map[string]interface{}', 'map[string]any'):
            props = {}
            for element in named(node, 'body').named_children:
                if element.type != 'keyed_element':
                    return None
                key, item = element.named_children[0], element.named_children[1]
                key = key.named_children[0] if key.type == 'literal_element' else key
                item = item.named_children[0] if item.type == 'literal_element' else item
                if key.type != 'interpreted_string_literal':
                    return None
                kind = self.type_of(item, types, path)
                if not kind:
                    return None
                try:
                    props[literal(key)] = self.im.schema(kind, direction='output')
                except Unsupported:
                    return None
            return object_schema(props, list(props))
        kind = self.type_of(node, types, path)
        if not kind:
            return None
        try:
            return self.im.schema(kind, direction='output')
        except Unsupported:
            return None
