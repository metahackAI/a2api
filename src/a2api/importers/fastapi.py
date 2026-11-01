"""FastAPI routes and Pydantic models, read with Python's `ast` module.

Nothing is imported or executed: modules are parsed, and names are followed through imports.
Routers are `APIRouter()`/`FastAPI()` objects; prefixes come from `APIRouter(prefix=...)` and
`include_router(router, prefix=...)` down from the application (a prefix read from a settings
class default is noted). Inputs come from the handler signature and the `Depends(...)` functions it
names: path placeholders, `Query`/`Path`/`Body`/`Header` parameters, scalar query parameters and
Pydantic body models (`Body(embed=True, alias=...)` included). Outputs come from `response_model`
or the return annotation, serialized by alias as FastAPI does. Pydantic aliases follow `Field(alias=)`
and the model's `alias_generator` when it is a known camel/pascal converter.
"""

from __future__ import annotations

import ast
import re

from .source import SourceImporter, Unsupported, object_schema, record

HTTP = {'get': 'GET', 'post': 'POST', 'put': 'PUT', 'patch': 'PATCH', 'delete': 'DELETE', 'head': 'HEAD'}
CONTEXT_TYPES = {'Request', 'Response', 'BackgroundTasks', 'WebSocket', 'HTTPConnection', 'Session', 'AsyncSession',
                 'Connection', 'SecurityScopes', 'HTTPAuthorizationCredentials'}
PARAMS = {'Path': 'path', 'Query': 'query', 'Body': 'body', 'Header': 'headers', 'Cookie': 'cookie', 'Form': 'form',
          'File': 'form', 'UploadFile': 'form'}
SCALARS = {'str': {'type': 'string'}, 'int': {'type': 'integer'}, 'float': {'type': 'number'}, 'bool': {'type': 'boolean'},
           'Decimal': {'type': 'number'}, 'datetime': {'type': 'string', 'format': 'date-time'},
           'date': {'type': 'string', 'format': 'date'}, 'time': {'type': 'string'}, 'UUID': {'type': 'string', 'format': 'uuid'},
           'EmailStr': {'type': 'string', 'format': 'email'}, 'HttpUrl': {'type': 'string', 'format': 'uri'},
           'AnyUrl': {'type': 'string', 'format': 'uri'}, 'AnyHttpUrl': {'type': 'string', 'format': 'uri'},
           'constr': {'type': 'string'}, 'conint': {'type': 'integer'}, 'SecretStr': {'type': 'string'},
           'PositiveInt': {'type': 'integer', 'minimum': 1}, 'NonNegativeInt': {'type': 'integer', 'minimum': 0}}
BOUNDS = {'ge': 'minimum', 'le': 'maximum', 'gt': 'exclusiveMinimum', 'lt': 'exclusiveMaximum', 'min_length': 'minLength',
          'max_length': 'maxLength', 'regex': 'pattern', 'pattern': 'pattern', 'min_items': 'minItems', 'max_items': 'maxItems'}


def _name(node):
    """`a.b.c` for Name/Attribute chains, else None."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _name(node.value)
        return base + '.' + node.attr if base else None
    return None


def _call_name(node):
    return _name(node.func) if isinstance(node, ast.Call) else None


def _keywords(call):
    return {item.arg: item.value for item in call.keywords if item.arg}


def _constant(node, default=None):
    return node.value if isinstance(node, ast.Constant) else default


def _status(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    found = re.search(r'HTTP_(\d{3})', _name(node) or '')
    return int(found[1]) if found else None


def _camel(name, upper_first=False):
    words = [w for w in name.split('_') if w]
    if not words:
        return name
    return ''.join(w.capitalize() if i or upper_first else w for i, w in enumerate(words))


class FastAPISourceImporter(SourceImporter):
    language, extension = 'python', '.py'
    skip_suffixes = ('_test.py', 'conftest.py')

    def _parser(self):
        def parse(raw):
            try:
                return ast.parse(raw)
            except (SyntaxError, ValueError):
                return None
        return parse

    # --- modules and names ------------------------------------------------------------------------

    def _index(self):
        self.modules = {}
        for path, unit in self.units:
            if re.search(r'(^|/)tests?/', path):
                continue
            dotted = re.sub(r'(/__init__)?\.py$', '', path).replace('/', '.').replace('\\', '.')
            self.modules[dotted] = unit
        self.symbols = {}
        for module, unit in self.modules.items():
            table = {}
            package = module if self._is_package(module) else module.rpartition('.')[0]
            for node in ast.walk(unit):
                if isinstance(node, ast.ImportFrom):
                    base = node.module or ''
                    if node.level:
                        parent = package.split('.') if package else []
                        parent = parent[:len(parent) - (node.level - 1)] if node.level > 1 else parent
                        base = '.'.join(filter(None, ['.'.join(parent), base]))
                    for alias in node.names:
                        table[alias.asname or alias.name] = ('from', base, alias.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        table[alias.asname or alias.name.split('.')[0]] = ('module', alias.name if alias.asname else alias.name.split('.')[0])
            for node in unit.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    table[node.name] = ('def', node)
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    for target in targets:
                        if isinstance(target, ast.Name) and node.value is not None:
                            table[target.id] = ('value', node.value)
            self.symbols[module] = table

    def _is_package(self, module):
        return any(path.replace('\\', '/').endswith('__init__.py') and re.sub(r'(/__init__)?\.py$', '', path).replace('/', '.') == module
                   for path, _ in self.units)

    def _module(self, dotted):
        """The known module a (possibly package-qualified) dotted name refers to."""
        if dotted in self.modules:
            return dotted
        parts = dotted.split('.')
        for start in range(1, len(parts)):
            candidate = '.'.join(parts[start:])
            if candidate in self.modules:
                return candidate
        return None

    def resolve(self, module, name, depth=0):
        """(module, ('def', node) | ('value', node) | ('module', name)) for a dotted name used in a module."""
        if depth > 12 or module is None:
            return None, None
        head, _, rest = name.partition('.')
        entry = self.symbols.get(module, {}).get(head)
        if entry is None:
            return None, None
        if entry[0] == 'from':
            target_module = self._module(entry[1] + '.' + entry[2]) if self._module(entry[1] + '.' + entry[2]) else None
            if target_module and rest:
                return self.resolve(target_module, rest, depth + 1)
            if target_module and not rest:
                return target_module, ('module', target_module)
            source = self._module(entry[1]) if entry[1] else None
            return self.resolve(source, entry[2] + ('.' + rest if rest else ''), depth + 1) if source else (None, None)
        if entry[0] == 'module':
            target_module = self._module(entry[1])
            if not rest:
                return target_module, ('module', target_module)
            return self.resolve(target_module, rest, depth + 1) if target_module else (None, None)
        if rest:
            return None, None
        return module, entry

    # --- routers ----------------------------------------------------------------------------------

    def _routers(self):
        """{(module, variable): own prefix} for every APIRouter()/FastAPI() assignment, and the apps."""
        routers, apps = {}, set()
        self._router_nodes = {}
        for module, unit in self.modules.items():
            for node in ast.walk(unit):
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    kind = (_call_name(node.value) or '').split('.')[-1]
                    if kind in ('APIRouter', 'FastAPI'):
                        prefix = _constant(_keywords(node.value).get('prefix'), '')
                        routers[(module, node.targets[0].id)] = prefix
                        self._router_nodes[id(node.value)] = (module, node.targets[0].id)
                        if kind == 'FastAPI':
                            apps.add((module, node.targets[0].id))
        return routers, apps

    def _router_ref(self, module, node, routers):
        name = _name(node)
        if name is None:
            return None
        if (module, name) in routers:
            return module, name
        _, entry = self.resolve(module, name)
        if entry and entry[0] == 'value':
            return self._router_nodes.get(id(entry[1]))
        return None

    def _prefix_value(self, node):
        value = _constant(node)
        if isinstance(value, str):
            return value
        name = _name(node)
        if name:
            # A settings object attribute: use a unique class-level default of that name, and say so.
            field = name.split('.')[-1]
            found = [item.value for unit in self.modules.values() for item in ast.walk(unit)
                     if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name) and item.target.id == field
                     and isinstance(_constant(item.value), str)]
            if len(found) == 1:
                self.warn('PREFIX_FROM_SETTINGS_DEFAULT', f'{name} is read as its settings default "{found[0].value}".')
                return found[0].value
        raise Unsupported('include_router prefix is not a literal or a settings default.')

    def _mounts(self, routers, apps):
        """{router: [full prefix]} walking include_router from the apps (or from never-included routers)."""
        edges = {}
        for module, unit in self.modules.items():
            for node in ast.walk(unit):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'include_router'):
                    continue
                parent = self._router_ref(module, node.func.value, routers)
                child = self._router_ref(module, node.args[0], routers) if node.args else None
                if parent and child:
                    edges.setdefault(parent, []).append((child, _keywords(node).get('prefix')))
        included = {child for children in edges.values() for child, _ in children}
        roots = sorted(apps) or sorted(set(routers) - included)
        mounts, pending = {}, [(root, routers[root]) for root in roots]
        while pending:
            router, prefix = pending.pop()
            mounts.setdefault(router, []).append(prefix)
            if len(mounts[router]) > 8:
                raise Unsupported('Router inclusion is cyclic or too deep.')
            for child, raw in edges.get(router, []):
                pending.append((child, prefix.rstrip('/') + ('/' + self._prefix_value(raw).strip('/') if raw is not None else '')
                                + (('/' + routers[child].strip('/')) if routers[child] else '')))
        return mounts

    def _extract(self):
        self._index()
        routers, apps = self._routers()
        try:
            mounts = self._mounts(routers, apps)
            pending = list(self._pending)
        except Unsupported as error:
            self.diagnostics.append({'code': 'SOURCE_UNSUPPORTED', 'detail': str(error)})
            return
        for module, unit in self.modules.items():
            for function in ast.walk(unit):
                if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for decorator in function.decorator_list:
                    if not (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute)):
                        continue
                    verb = decorator.func.attr
                    router = self._router_ref(module, decorator.func.value, routers)
                    if router is None or (verb not in HTTP and verb != 'api_route'):
                        continue
                    options = _keywords(decorator)
                    raw_path = _constant(decorator.args[0]) if decorator.args else _constant(options.get('path'))
                    verbs = [HTTP[verb]] if verb in HTTP else [str(_constant(item, '')).upper() for item in
                                                               getattr(options.get('methods'), 'elts', [])]
                    location = f'{module.replace(".", "/")}.py:{function.lineno}'
                    for prefix in mounts.get(router, []):
                        for method in verbs:
                            route = ''
                            self._pending = list(pending)
                            try:
                                if not isinstance(raw_path, str) or method not in HTTP.values():
                                    raise Unsupported('Route decorators need a literal path and HTTP method.')
                                route = re.sub(r'/+', '/', '/' + prefix.strip('/') + '/' + raw_path.strip('/')).rstrip('/') or '/'
                                if re.search(r'\{[^}]*:path\}', route):
                                    raise Unsupported('Path converters need an explicit binding.')
                                yield self._route(function, module, method, route, options, location)
                            except (Unsupported, AttributeError, TypeError, IndexError, KeyError) as error:
                                yield self.unsupported(function.name, route, method, location, str(error))

    # --- handlers ---------------------------------------------------------------------------------

    def _route(self, function, module, method, route, options, location):
        placeholders = re.findall(r'\{([^{}:]+)\}', route)
        groups = {'path': {}, 'query': {}, 'headers': {}}
        required = {'path': [], 'query': [], 'headers': []}
        bodies, context = [], []
        self._parameters(function, module, placeholders, groups, required, bodies, context, depth=0)
        for dependency in getattr(options.get('dependencies'), 'elts', []):
            # Route-level dependencies read request values too (and often only check permissions).
            target = dependency.args[0] if isinstance(dependency, ast.Call) and dependency.args else None
            target_module, entry = self.resolve(module, _name(target)) if _name(target) else (None, None)
            if entry and entry[0] == 'def' and isinstance(entry[1], (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._parameters(entry[1], target_module, placeholders, groups, required, bodies, context, depth=1)
        missing = set(placeholders) - set(groups['path'])
        for name in missing:  # a placeholder no parameter reads is still part of the URL
            groups['path'][name] = {'type': 'string'}
            required['path'].append(name)
        if context:
            self.warn('CONTEXT_DEPENDENCY', 'Supplied by the server, not the caller: ' + ', '.join(sorted(set(context))) + '.')
        inputs, needed, paths, queries, headers = {}, [], {}, {}, {}
        for group in ('path', 'query', 'headers'):
            if groups[group]:
                inputs[group] = object_schema(groups[group], sorted(set(required[group])))
                if required[group]:
                    needed.append(group)
        paths = {name: '/path/' + name for name in groups['path']}
        queries = {name: {'pointer': '/query/' + name, 'required': name in required['query'], 'explode': True}
                   for name in groups['query']}
        headers = {name: {'pointer': '/headers/' + name, 'required': name in required['headers']} for name in groups['headers']}
        has_body = bool(bodies)
        if has_body:
            if len(bodies) == 1 and not bodies[0][3]:
                _, schema, body_required, _ = bodies[0]
                inputs['body'] = schema
            else:
                inputs['body'] = object_schema({key: schema for key, schema, _, _ in bodies},
                                               [key for key, _, needed_, _ in bodies if needed_])
                body_required = any(needed_ for _, _, needed_, _ in bodies)
            if body_required:
                needed.append('body')
        status = _status(options['status_code']) if 'status_code' in options else 200
        if status is None:
            raise Unsupported('status_code must be a literal status.')
        if ('response_class' in options and status not in (204, 205)
                and not re.search(r'JSON', _name(options['response_class']) or '')):
            raise Unsupported('Non-JSON response classes need an explicit codec.')
        if status in (204, 205) or method == 'HEAD':
            output = {'type': 'null'}
        else:
            annotation = options.get('response_model', function.returns)
            if annotation is None or isinstance(annotation, ast.Constant) and annotation.value is None:
                output = self.open_output('No response_model or return annotation')
            else:
                try:
                    output = self.type_schema(annotation, module, direction='output')
                except Unsupported as error:
                    output = self.open_output(str(error))
        summary = _constant(options.get('summary')) or _constant(options.get('name')) or (ast.get_docstring(function) or '').split('\n')[0] or None
        return record(self.namespace, function.name, route, method, object_schema(inputs, needed), output, location,
                      title=summary, statuses=(status,), path_bindings=paths, query_bindings=queries,
                      header_bindings=headers, body=has_body, body_required=has_body and 'body' in needed)

    def _parameters(self, function, module, placeholders, groups, required, bodies, context, depth):
        if depth > 6:
            raise Unsupported('Dependencies are nested too deeply.')
        arguments = function.args
        positional = arguments.posonlyargs + arguments.args
        defaults = [None] * (len(positional) - len(arguments.defaults)) + list(arguments.defaults)
        pairs = list(zip(positional, defaults)) + list(zip(arguments.kwonlyargs, arguments.kw_defaults))
        for argument, default in pairs:
            name, annotation = argument.arg, argument.annotation
            if name in ('self', 'cls'):
                continue
            kind = (_call_name(default) or '').split('.')[-1] if isinstance(default, ast.Call) else ''
            type_name = (_name(annotation) or '').split('.')[-1] if annotation is not None else ''
            if kind in ('Depends', 'Security'):
                dependency = default.args[0] if default.args else annotation
                target_module, entry = self.resolve(module, _name(dependency)) if _name(dependency) else (None, None)
                if entry and entry[0] == 'def' and isinstance(entry[1], (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self._parameters(entry[1], target_module, placeholders, groups, required, bodies, context, depth + 1)
                else:
                    context.append(name)  # a dependency factory or class: supplied by the server
                continue
            if type_name in CONTEXT_TYPES:
                continue
            options = _keywords(default) if kind in PARAMS else {}
            if kind in PARAMS:
                first = default.args[0] if default.args else options.get('default')
                is_required = first is None or isinstance(first, ast.Constant) and first.value is Ellipsis
                literal_default = None if is_required else _constant(first)
            else:
                is_required = default is None
                literal_default = _constant(default)
            where = PARAMS.get(kind)
            if where is None:
                if name in placeholders:
                    where = 'path'
                elif self._is_model(annotation, module):
                    where = 'body'
                else:
                    where = 'query'
            if where in ('cookie',):
                context.append(name)
                continue
            if where == 'form':
                raise Unsupported('Form/file parameters are outside the JSON profile.')
            schema = self.type_schema(annotation, module, direction='input') if annotation is not None else {}
            optional = 'anyOf' in schema and {'type': 'null'} in schema['anyOf']
            if where in ('path', 'query', 'headers') and optional:
                schema = next(item for item in schema['anyOf'] if item != {'type': 'null'})
                is_required = False
            for key, keyword in BOUNDS.items():
                if key in options and _constant(options[key]) is not None:
                    schema[keyword] = _constant(options[key])
            if literal_default is not None and where != 'body':
                schema['default'] = literal_default
            key = _constant(options.get('alias')) or (name.replace('_', '-') if where == 'headers' else name)
            if where == 'headers' and key.lower() in ('authorization', 'cookie'):
                context.append(name)
                continue
            if where == 'body':
                embed = _constant(options.get('embed'), False) or 'alias' in options
                bodies.append((key, schema, is_required, bool(embed)))
                continue
            if where == 'path':
                if name not in placeholders and key not in placeholders:
                    raise Unsupported(f'Path parameter {name} is not in the route.')
                is_required = True
            groups[where][key] = schema
            if is_required:
                required[where].append(key)

    # --- types ------------------------------------------------------------------------------------

    def _is_model(self, annotation, module):
        if annotation is None:
            return False
        if isinstance(annotation, ast.Subscript):
            outer = (_name(annotation.value) or '').split('.')[-1]
            if outer in ('Optional', 'Annotated'):
                inner = annotation.slice.elts[0] if isinstance(annotation.slice, ast.Tuple) else annotation.slice
                return self._is_model(inner, module)
            return False
        name = _name(annotation)
        if not name:
            return False
        owner, entry = self.resolve(module, name)
        return bool(entry and entry[0] == 'def' and isinstance(entry[1], ast.ClassDef) and self._model_bases(entry[1], owner))

    def _model_bases(self, cls, module, depth=0):
        """True when a class reaches pydantic BaseModel through its bases."""
        if depth > 16:
            return False
        for base in cls.bases:
            name = _name(base) or ''
            if name.split('.')[-1] in ('BaseModel', 'BaseSettings', 'GenericModel', 'RootModel'):
                return True
            owner, entry = self.resolve(module, name)
            if entry and entry[0] == 'def' and isinstance(entry[1], ast.ClassDef) and self._model_bases(entry[1], owner, depth + 1):
                return True
        return False

    def type_schema(self, node, module, *, direction, stack=()):
        if isinstance(node, ast.Constant):
            if node.value is None:
                return {'type': 'null'}
            if isinstance(node.value, str):  # a forward reference
                return self.type_schema(ast.parse(node.value, mode='eval').body, module, direction=direction, stack=stack)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            return self._union([node.left, node.right], module, direction, stack)
        if isinstance(node, ast.Subscript):
            outer = (_name(node.value) or '').split('.')[-1]
            items = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
            if outer == 'Optional':
                return {'anyOf': [self.type_schema(items[0], module, direction=direction, stack=stack), {'type': 'null'}]}
            if outer == 'Union':
                return self._union(items, module, direction, stack)
            if outer in ('List', 'list', 'Sequence', 'Set', 'set', 'FrozenSet', 'frozenset', 'Iterable'):
                return {'type': 'array', 'items': self.type_schema(items[0], module, direction=direction, stack=stack)}
            if outer in ('Dict', 'dict', 'Mapping') and len(items) == 2 and _name(items[0]) == 'str':
                return {'type': 'object', 'additionalProperties': self.type_schema(items[1], module, direction=direction, stack=stack)}
            if outer == 'Literal':
                return {'enum': [_constant(item) for item in items]}
            if outer == 'Annotated':
                return self.type_schema(items[0], module, direction=direction, stack=stack)
            raise Unsupported(f'Unsupported Python type: {ast.unparse(node)}')
        name = _name(node)
        if name is None:
            raise Unsupported(f'Unsupported Python type: {ast.unparse(node)}')
        short = name.split('.')[-1]
        if short in SCALARS:
            return dict(SCALARS[short])
        if short in ('Any', 'object', 'Json') and direction == 'output':
            return {}
        if short in ('dict', 'Dict') and direction == 'output':
            return {'type': 'object'}
        if short in ('list', 'List') and direction == 'output':
            return {'type': 'array'}
        owner, entry = self.resolve(module, name)
        if not entry or entry[0] != 'def' or not isinstance(entry[1], ast.ClassDef):
            raise Unsupported(f'Unresolved Python type: {name}')
        cls = entry[1]
        if any((_name(base) or '').split('.')[-1] in ('Enum', 'IntEnum', 'StrEnum') for base in cls.bases):
            values = [_constant(item.value) for item in cls.body if isinstance(item, ast.Assign)]
            return {'enum': [value for value in values if value is not None]}
        if not self._model_bases(cls, owner):
            raise Unsupported(f'{name} is not a Pydantic model.')
        return self._model(cls, owner, direction, stack)

    def _union(self, items, module, direction, stack):
        branches = [self.type_schema(item, module, direction=direction, stack=stack) for item in items]
        values = [branch for branch in branches if branch != {'type': 'null'}]
        if len(values) == 1:
            return {'anyOf': [values[0], {'type': 'null'}]} if len(branches) > 1 else values[0]
        return {'anyOf': branches}

    def _alias_generator(self, cls, module, depth=0):
        """The model's alias function as 'camel'|'pascal'|None, following Config/model_config and bases."""
        if depth > 16:
            return None
        for item in cls.body:
            value = None
            if isinstance(item, ast.ClassDef) and item.name == 'Config':
                for statement in item.body:
                    if isinstance(statement, ast.Assign) and any(_name(t) == 'alias_generator' for t in statement.targets):
                        value = statement.value
                if value is None:
                    for base in item.bases:  # class Config(RWModel.Config)
                        owner, entry = self.resolve(module, (_name(base) or '').rsplit('.', 1)[0])
                        if entry and entry[0] == 'def' and isinstance(entry[1], ast.ClassDef):
                            found = self._alias_generator(entry[1], owner, depth + 1)
                            if found:
                                return found
            elif isinstance(item, ast.Assign) and any(_name(t) == 'model_config' for t in item.targets):
                if isinstance(item.value, ast.Call):
                    value = _keywords(item.value).get('alias_generator')
                elif isinstance(item.value, ast.Dict):
                    value = dict(zip([_constant(k) for k in item.value.keys], item.value.values)).get('alias_generator')
            if value is not None:
                return self._generator_kind(value, module)
        for base in cls.bases:
            owner, entry = self.resolve(module, _name(base) or '')
            if entry and entry[0] == 'def' and isinstance(entry[1], ast.ClassDef):
                found = self._alias_generator(entry[1], owner, depth + 1)
                if found:
                    return found
        return None

    def _generator_kind(self, value, module):
        name = _name(value) or ''
        short = name.split('.')[-1]
        if short in ('to_camel', 'to_lower_camel', 'camelize'):
            return 'camel'
        if short == 'to_pascal':
            return 'pascal'
        owner, entry = self.resolve(module, name)
        if entry and entry[0] == 'def' and isinstance(entry[1], (ast.FunctionDef, ast.AsyncFunctionDef)):
            source = ast.unparse(entry[1])
            if re.search(r"split\(['\"]_['\"]\)", source) and re.search(r'capitalize|title\(\)|upper\(\)', source):
                return 'camel' if re.search(r'index == 0|i == 0|\[0\]|enumerate|\[1:\]', source) else 'pascal'
        raise Unsupported(f'alias_generator {name or ast.unparse(value)} is not a known camel/pascal converter.')

    def _model(self, cls, module, direction, stack):
        key = (module, cls.name)
        if key in stack or len(stack) > 32:
            raise Unsupported('Recursive models need an explicit finite schema.')
        fields = self._fields(cls, module, direction, stack + (key,), self._alias_generator(cls, module))
        props = {alias: schema for alias, (schema, _, _) in fields.items()}
        required = [alias for alias, (_, needed, _) in fields.items() if needed] if direction == 'input' else []
        return object_schema(props, required)

    def _fields(self, cls, module, direction, stack, generator, depth=0):
        """{alias: (schema, required, attribute)} in pydantic order: bases (last to first), then the class."""
        if depth > 16:
            raise Unsupported('Model inheritance is too deep.')
        fields = {}
        for base in reversed(cls.bases):
            owner, entry = self.resolve(module, _name(base) or '')
            if entry and entry[0] == 'def' and isinstance(entry[1], ast.ClassDef):
                for alias, value in self._fields(entry[1], owner, direction, stack, generator, depth + 1).items():
                    fields = {k: v for k, v in fields.items() if v[2] != value[2]}
                    fields[alias] = value
        for item in cls.body:
            if not isinstance(item, ast.AnnAssign) or not isinstance(item.target, ast.Name):
                continue
            name = item.target.id
            if name.startswith('_') or (_name(getattr(item.annotation, 'value', item.annotation)) or '').endswith('ClassVar'):
                continue
            alias, needed = None, item.value is None
            if isinstance(item.value, ast.Call) and (_call_name(item.value) or '').split('.')[-1] == 'Field':
                options = _keywords(item.value)
                alias = _constant(options.get('alias')) or _constant(
                    options.get('serialization_alias' if direction == 'output' else 'validation_alias'))
                first = item.value.args[0] if item.value.args else options.get('default')
                needed = ((first is None and 'default_factory' not in options)
                          or (isinstance(first, ast.Constant) and first.value is Ellipsis))
            schema = self.type_schema(item.annotation, module, direction=direction, stack=stack)
            if needed and item.value is None and 'anyOf' in schema and {'type': 'null'} in schema['anyOf']:
                needed = False  # Optional[...] without a default defaults to None (pydantic v1)
            key = alias or (_camel(name) if generator == 'camel' else _camel(name, True) if generator == 'pascal' else name)
            fields = {k: v for k, v in fields.items() if v[2] != name}
            fields[key] = (schema, needed, name)
        return fields
