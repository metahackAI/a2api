"""Static Spring MVC route and local Java DTO extraction, without OpenAPI.

Besides typed DTO signatures, real controllers often return a raw `ResponseEntity` built from a
service call or a `new HashMap<>() {{ put("article", data); }}`. The importer follows those
expressions through controller fields, local variables, lambda parameters, `Optional` and
same-class helper methods to the declared Java types. What cannot be followed is never guessed:
the operation is unsupported, or (untyped_output='open') imported with an open output schema.
Jackson settings in application.properties/yml (root wrapping, naming strategy, inclusion) are
applied to bodies and DTO fields.
"""

import re

from .source import SourceImporter, Unsupported, literal, named, object_schema, record, split_types, text, walk


def annotations(node):
    result = {}
    modifiers = next((child for child in node.named_children if child.type == 'modifiers'), None)
    if modifiers is None:
        return result
    for annotation in modifiers.named_children:
        if annotation.type not in ('annotation', 'marker_annotation'):
            continue
        name = text(named(annotation, 'name')).split('.')[-1]
        arguments = named(annotation, 'arguments')
        values = {}
        for arg in arguments.named_children if arguments else ():
            if arg.type == 'element_value_pair':
                values[text(named(arg, 'key'))] = named(arg, 'value')
            else:
                values['value'] = arg
        result[name] = values
    return result


def value(annotation, key='value', default=None):
    node = annotation.get(key)
    return literal(node) if node else default


STATUS = {'OK': 200, 'CREATED': 201, 'ACCEPTED': 202, 'NO_CONTENT': 204, 'RESET_CONTENT': 205, 'PARTIAL_CONTENT': 206}
RESPONSE_STATUS = {'ok': 200, 'created': 201, 'accepted': 202, 'noContent': 204}
UNTYPED = ('Map', 'HashMap', 'LinkedHashMap', 'TreeMap', 'Object', 'JsonNode', 'ObjectNode')
# Jackson annotations whose effect is modelled here; any other Json* annotation needs an explicit schema.
CLASS_JACKSON = ('JsonIgnoreProperties', 'JsonRootName', 'JsonInclude', 'JsonPropertyOrder')
FIELD_JACKSON = ('JsonProperty', 'JsonIgnore', 'JsonInclude', 'JsonFormat')
DATE_TIMES = ('OffsetDateTime', 'Instant', 'ZonedDateTime', 'DateTime', 'Date', 'Timestamp')
NOT_INFERRED = object()


def _decapitalize(name):
    return name[:1].lower() + name[1:] if not name[1:2].isupper() else name


def _snake(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).lower()


def _returns(node):
    """Return statements of one method or lambda body, without those of nested lambdas or classes."""
    found, pending = [], list(reversed(node.named_children))
    while pending:
        current = pending.pop()
        if current.type == 'return_statement':
            found.append(current)
        elif current.type not in ('lambda_expression', 'class_body'):
            pending.extend(reversed(current.named_children))
    return found


def _flatten_settings(data, prefix=''):
    if isinstance(data, dict):
        for key, item in data.items():
            yield from _flatten_settings(item, f'{prefix}.{key}' if prefix else str(key))
    else:
        yield prefix, data


class SpringSourceImporter(SourceImporter):
    language, extension = 'java', '.java'

    def _extract(self):
        self.models = {}
        self.jackson = self._jackson()
        blocking = []
        for _, unit in self.units:
            for node in walk(unit):
                if node.type in ('class_declaration', 'record_declaration', 'enum_declaration', 'interface_declaration'):
                    self.models.setdefault(text(named(node, 'name')), []).append(node)
                    advice = {'RestControllerAdvice', 'ControllerAdvice'} & annotations(node).keys()
                    interfaces = text(named(node, 'interfaces')) if named(node, 'interfaces') else ''
                    if re.search(r'\b(ResponseBodyAdvice|RequestBodyAdvice)\b', interfaces):
                        blocking.append('Body advice rewrites request/response bodies; describe them explicitly.')
                    elif advice and node.type == 'class_declaration' and any(
                            {'InitBinder', 'ModelAttribute'} & annotations(member).keys()
                            for member in named(node, 'body').named_children if member.type == 'method_declaration'):
                        blocking.append('Controller advice binders change request binding; describe it explicitly.')
        for path, unit in self.units:
            for controller in walk(unit, 'class_declaration'):
                declared = annotations(controller)
                if 'RestController' not in declared:
                    continue
                base = declared.get('RequestMapping', {})
                for method in named(controller, 'body').named_children:
                    if method.type != 'method_declaration':
                        continue
                    attrs = annotations(method)
                    mappings = [key for key in attrs if key in ('RequestMapping', 'GetMapping', 'PostMapping', 'PutMapping', 'PatchMapping', 'DeleteMapping')]
                    if not mappings:
                        continue
                    opid = text(named(controller, 'name')) + '.' + text(named(method, 'name'))
                    location = f'{path}:{method.start_point.row + 1}'
                    route, verb = '', ''
                    try:
                        if blocking:
                            raise Unsupported(blocking[0])
                        if len(mappings) != 1:
                            raise Unsupported('Multiple method mappings require explicit selection.')
                        mapping = mappings[0]
                        options = attrs[mapping]
                        if {'params', 'headers'} & (base.keys() | options.keys()):
                            raise Unsupported('Conditional request mapping needs an explicit binding.')
                        prefix = value(base, 'path', value(base, default='')) or ''
                        suffix = value(options, 'path', value(options, default='')) or ''
                        route = (('/' + prefix.strip('/') if prefix.strip('/') else '')
                                 + ('/' + suffix.lstrip('/') if suffix else '')) or '/'
                        if mapping == 'RequestMapping':
                            raw = options.get('method') or base.get('method')
                            if raw is None:
                                raise Unsupported('RequestMapping needs one explicit HTTP method.')
                            if raw.type == 'element_value_array_initializer' and len(raw.named_children) == 1:
                                raw = raw.named_children[0]
                            verb = text(raw).split('.')[-1]
                        else:
                            verb = mapping.removesuffix('Mapping').upper()
                        if 'consumes' in options and value(options, 'consumes') != 'application/json':
                            raise Unsupported('Only JSON request bodies are supported.')
                        if 'produces' in options and value(options, 'produces') != 'application/json':
                            raise Unsupported('Only JSON/empty responses are supported.')
                        if any(key in declared or key in attrs for key in ('Profile', 'ConditionalOnProperty')):
                            raise Unsupported('Conditional controller activation requires host-specific selection.')
                        yield self._method(opid, route, verb, method, attrs, location, controller)
                    except (Unsupported, AttributeError, TypeError) as error:
                        yield self.unsupported(opid, route, verb, location, str(error) or 'Unsupported mapping syntax.')

    def _jackson(self):
        """spring.jackson.* settings from application properties/YAML near the sources."""
        settings = {}
        config = lambda paths: sorted(p for p in paths if p.suffix in ('.properties', '.yml', '.yaml') and 'test' not in p.parts)[:8]
        files = config(self.root.rglob('application*'))
        for parent in (self.root.parent, self.root.parent.parent):
            files = files or config(parent.glob('resources/application*'))
        for path in files:
            if path.is_symlink() or path.stat().st_size > 256 * 1024:
                continue
            raw = path.read_text(errors='replace')
            if path.suffix == '.properties':
                pairs = (line.split('=', 1) for line in raw.splitlines() if '=' in line and not line.lstrip().startswith(('#', '!')))
            else:
                try:
                    import yaml
                    pairs = _flatten_settings(yaml.safe_load(raw) or {})
                except Exception:
                    self.diagnostics.append({'code': 'SOURCE_CONFIG_UNREADABLE', 'location': path.name})
                    continue
            for key, item in pairs:
                key = str(key).strip().lower().replace('-', '_')
                if key.startswith('spring.jackson.'):
                    settings[key[len('spring.jackson.'):]] = str(item).strip().lower()
        code_customized = any(re.search(r'\b(UNWRAP_ROOT_VALUE|WRAP_ROOT_VALUE|PropertyNamingStrateg|setSerializationInclusion)\b', text(unit))
                              for _, unit in self.units)
        return {'unwrap': settings.get('deserialization.unwrap_root_value') == 'true',
                'wrap': settings.get('serialization.wrap_root_value') == 'true',
                'naming': settings.get('property_naming_strategy', ''),
                'non_null': settings.get('default_property_inclusion') in ('non_null', 'non_absent', 'non_empty'),
                'code': code_customized}

    def _name(self, original):
        naming = self.jackson['naming'].rsplit('.', 1)[-1]
        if naming in ('', 'lower_camel_case'):
            return original
        if naming in ('snake_case', 'snakecasestrategy'):
            return _snake(original)
        raise Unsupported('Unsupported Jackson property naming strategy: ' + naming)

    def _root_name(self, typename):
        name = re.sub(r'<.*', '', typename).split('.')[-1]
        choices = self.models.get(name, [])
        root = value(annotations(choices[0]).get('JsonRootName', {}), default=None) if len(choices) == 1 else None
        return root or name

    def schema(self, typename, *, stack=(), substitutions=None, validate=False, output=False):
        substitutions = substitutions or {}
        typename = substitutions.get(typename.strip(), typename.strip())
        typename = re.sub(r'^(final\s+)', '', typename)
        if len(stack) > 32 or typename in stack:
            raise Unsupported('Recursive/deep DTOs need an explicit finite wrapper.')
        if typename.endswith('[]'):
            return {'type': 'array', 'items': self.schema(typename[:-2], stack=stack, output=output)}
        match = re.fullmatch(r'([\w.]+)(?:<(.*)>)?', typename)
        if not match:
            raise Unsupported('Unsupported Java type: ' + typename)
        name, arguments = match.groups()
        name = name.split('.')[-1]
        args = split_types(arguments) if arguments else []
        primitives = {'String': 'string', 'char': 'string', 'Character': 'string', 'boolean': 'boolean', 'Boolean': 'boolean',
                      'int': 'integer', 'Integer': 'integer', 'long': 'integer', 'Long': 'integer', 'short': 'integer',
                      'Short': 'integer', 'byte': 'integer', 'Byte': 'integer', 'double': 'number', 'Double': 'number',
                      'float': 'number', 'Float': 'number', 'BigDecimal': 'number', 'BigInteger': 'integer'}
        if name in primitives:
            return {'type': primitives[name]}
        if name in ('void', 'Void'):
            return {'type': 'null'}
        if name == 'LocalDateTime':
            return {'type': 'string', 'description': 'ISO local date-time without a UTC offset.'}
        if name in ('LocalDate', 'OffsetDateTime', 'Instant'):
            return {'type': 'string', 'format': 'date' if name == 'LocalDate' else 'date-time'}
        if name in DATE_TIMES:
            # Its JSON form depends on the ObjectMapper's modules and timestamp settings.
            return {'description': 'Date-time; its JSON form depends on the service Jackson configuration.'}
        if name in ('UUID',):
            return {'type': 'string', 'format': 'uuid'}
        if name in ('List', 'Set', 'Collection', 'ArrayList', 'LinkedList', 'HashSet') and len(args) == 1:
            return {'type': 'array', 'items': self.schema(args[0], stack=stack, substitutions=substitutions, validate=validate, output=output)}
        if name in ('Map', 'HashMap', 'LinkedHashMap', 'TreeMap') and len(args) == 2 and args[0] == 'String' and args[1] != 'Object':
            return {'type': 'object', 'additionalProperties': self.schema(args[1], stack=stack, substitutions=substitutions,
                                                                          validate=validate, output=output)}
        if name == 'ResponseEntity' and len(args) == 1:
            return self.schema(args[0], stack=stack, validate=validate, output=output)
        if name == 'Optional' and len(args) == 1:
            return {'anyOf': [self.schema(args[0], stack=stack, validate=validate, output=output), {'type': 'null'}]}
        choices = [choice for choice in self.models.get(name, []) if choice.type != 'interface_declaration']
        if len(choices) != 1:
            raise Unsupported('Unresolved or ambiguous Java DTO: ' + name)
        model = choices[0]
        attrs = annotations(model)
        if any(key.startswith('Json') and key not in CLASS_JACKSON for key in attrs):
            raise Unsupported('Class-level custom Jackson behavior needs an explicit schema.')
        if set(attrs.get('JsonIgnoreProperties', {})) - {'ignoreUnknown'}:
            raise Unsupported('Class-level Jackson property filters need an explicit schema.')
        if model.type == 'enum_declaration':
            if any(child.type == 'enum_body_declarations' for child in named(model, 'body').named_children):
                raise Unsupported('Custom enum serialization cannot be inferred.')
            return {'type': 'string', 'enum': [text(named(c, 'name')) for c in named(model, 'body').named_children if c.type == 'enum_constant']}
        parameters = named(model, 'type_parameters')
        typevars = [text(named(p, 'name')) or text(p) for p in parameters.named_children] if parameters else []
        if len(typevars) != len(args):
            raise Unsupported('Generic DTO needs concrete type arguments: ' + name)
        substitutions = {**substitutions, **dict(zip(typevars, args))}
        props, required, implicit = {}, [], set()
        parent = named(model, 'superclass')
        if parent:
            inherited = self.schema(text(parent.named_children[0]), stack=stack + (typename,), substitutions=substitutions,
                                    validate=validate, output=output)
            props.update(inherited['properties']); required.extend(inherited['required'])
        lombok = bool({'Getter', 'Data', 'Value'} & attrs.keys())
        members = named(model, 'body').named_children
        getters = {text(named(c, 'name')): c for c in members if c.type == 'method_declaration'}
        fields = named(model, 'parameters').named_children if model.type == 'record_declaration' else members
        for field in fields:
            if field.type not in ('field_declaration', 'formal_parameter'):
                continue
            modifiers = next((c for c in field.named_children if c.type == 'modifiers'), None)
            if modifiers and any(token in text(modifiers).split() for token in ('static', 'transient')):
                continue
            ann = annotations(field)
            if 'JsonIgnore' in ann and value(ann['JsonIgnore'], default=True):
                continue
            if any(key.startswith('Json') and key not in FIELD_JACKSON for key in ann):
                raise Unsupported('Custom Jackson field behavior needs an explicit schema.')
            if set(ann.get('JsonProperty', {})) - {'value', 'required'}:
                raise Unsupported('Directional Jackson field behavior needs an explicit contract.')
            type_name = text(named(field, 'type'))
            variables = [c for c in field.named_children if c.type == 'variable_declarator'] if field.type == 'field_declaration' else [field]
            for variable in variables:
                original = text(named(variable, 'name'))
                public_field = modifiers is not None and 'public' in text(modifiers).split()
                if (model.type != 'record_declaration' and not public_field and 'JsonProperty' not in ann and not lombok
                        and 'get' + original[:1].upper() + original[1:] not in getters
                        and 'is' + original[:1].upper() + original[1:] not in getters):
                    if output:
                        continue  # Jackson does not serialize a private field without an accessor.
                    raise Unsupported('DTO field access needs a public field/getter, record, Lombok Getter/Data or JsonProperty.')
                field_name = value(ann.get('JsonProperty', {}), default=None) or self._name(original)
                if field_name in props:
                    raise Unsupported('Shadowed or duplicate JSON fields need an explicit schema.')
                if 'JsonFormat' in ann:
                    item = {'type': 'string'}
                else:
                    item = self.schema(type_name, stack=stack + (typename,), substitutions=substitutions,
                                       validate=validate and 'Valid' in ann, output=output)
                if validate:
                    if any(key in ann for key in ('NotNull', 'NotBlank', 'NotEmpty')):
                        required.append(field_name)
                    if 'NotBlank' in ann:
                        item.update(minLength=1, pattern=r'\S')
                    if 'NotEmpty' in ann:
                        if item.get('type') not in ('string', 'array'):
                            raise Unsupported('NotEmpty requires a supported string/collection type.')
                        item['minItems' if item['type'] == 'array' else 'minLength'] = 1
                    if 'Size' in ann:
                        suffix = 'Items' if item.get('type') == 'array' else 'Length'
                        for bound in ('min', 'max'):
                            if bound in ann['Size']:
                                item[bound + suffix] = value(ann['Size'], bound)
                    for bound, keyword in [('Min', 'minimum'), ('Max', 'maximum')]:
                        if bound in ann:
                            item[keyword] = value(ann[bound])
                    if 'Email' in ann and item.get('type') == 'string':
                        item['format'] = 'email'
                # Reference fields can be null; @Valid + non-null constraints close
                # that branch. Primitive fields always have a concrete zero value.
                primitive = type_name in ('char', 'boolean', 'int', 'long', 'short', 'byte', 'double', 'float')
                if (not primitive and not (validate and {'NotNull', 'NotBlank', 'NotEmpty'} & ann.keys())
                        and 'anyOf' not in item and item.get('type')):
                    item = {'anyOf': [item, {'type': 'null'}]}
                description = ann.get('Schema', {}).get('description')
                if description and description.type == 'string_literal':
                    item['description'] = literal(description)
                props[field_name] = item
                implicit.add(original)
        if output and model.type == 'class_declaration':
            # Jackson also serializes public no-argument getters that have no field.
            covered = set(props) | {self._name(name) for name in implicit}
            for method_name, method in getters.items():
                found = re.fullmatch(r'(get|is)([A-Z]\w*)', method_name)
                modifiers = next((c for c in method.named_children if c.type == 'modifiers'), None)
                words = text(modifiers).split() if modifiers else []
                if (not found or 'public' not in words or 'static' in words or named(method, 'parameters').named_children
                        or 'JsonIgnore' in annotations(method) or method_name == 'getClass'):
                    continue
                implicit_name = _decapitalize(found[2])
                key = value(annotations(method).get('JsonProperty', {}), default=None) or self._name(implicit_name)
                if key in covered or implicit_name in implicit:
                    continue
                try:
                    props[key] = self.schema(text(named(method, 'type')), stack=stack + (typename,), substitutions=substitutions, output=True)
                except Unsupported:
                    props[key] = {}
                    self.warn('OUTPUT_PROPERTY_UNTYPED', f'{name}.{method_name}() is serialized as "{key}"; its type is not read.')
        return object_schema(props, required)

    # --- following a raw ResponseEntity body to declared types -------------------------------------

    def _class_members(self, cls):
        fields, methods = {}, {}
        for member in named(cls, 'body').named_children:
            if member.type == 'field_declaration':
                for variable in (c for c in member.named_children if c.type == 'variable_declarator'):
                    fields[text(named(variable, 'name'))] = text(named(member, 'type'))
            elif member.type == 'method_declaration':
                methods.setdefault(text(named(member, 'name')), []).append(member)
        return fields, methods

    def _scope(self, method):
        scope = {}
        parameters = named(method, 'parameters')
        for param in parameters.named_children if parameters else ():
            if param.type == 'formal_parameter':
                scope[text(named(param, 'name'))] = text(named(param, 'type'))
        body = named(method, 'body')
        for declaration in walk(body, 'local_variable_declaration') if body else ():
            for variable in (c for c in declaration.named_children if c.type == 'variable_declarator'):
                scope.setdefault(text(named(variable, 'name')), text(named(declaration, 'type')))
        return scope

    def _declared(self, typename):
        """A declared Java type as ('optional'|'response'|'value', inner), or None when the declaration does
        not say its JSON (raw ResponseEntity, Map, Object). A declared type whose schema cannot be read is
        ('value', None): unknown, an error only where its JSON is needed."""
        typename = re.sub(r'^final\s+', '', (typename or '').strip())
        match = re.fullmatch(r'([\w.]+)(?:<(.*)>)?', typename)
        if not match:
            return None
        name, args = match[1].split('.')[-1], split_types(match[2]) if match[2] else []
        if name == 'Optional' and len(args) == 1:
            return ('optional', self._declared(args[0]) or ('value', None))
        if name == 'ResponseEntity':
            inner = self._declared(args[0]) if args and args[0].strip() not in ('?', 'Object') else None
            return ('response', inner) if inner else None
        if name in UNTYPED or name in ('var', '?'):
            return None
        try:
            return ('value', self.schema(typename, output=True))
        except Unsupported:
            return ('value', None)

    def _method_result(self, cls, method, depth, statuses):
        declared = self._declared(text(named(method, 'type')))
        if declared is not None or depth > 6:
            return declared
        scope = self._scope(method)
        results = [self._infer(named(ret, 'value') if named(ret, 'value') else ret.named_children[0], cls, scope, depth + 1, statuses)
                   for ret in _returns(named(method, 'body')) if ret.named_children]
        if not results or any(result is None for result in results) or any(result != results[0] for result in results):
            return None
        return results[0]

    def _receiver_type(self, node, cls, scope):
        if node.type == 'identifier':
            name = text(node)
            fields, _ = self._class_members(cls)
            if isinstance(scope.get(name), str):
                return scope[name]
            return fields.get(name, name if name[:1].isupper() else None)
        if node.type == 'field_access' and text(named(node, 'object')) == 'this':
            return self._class_members(cls)[0].get(text(named(node, 'field')))
        return None

    def _call_target(self, typename, name, arity):
        if not typename:
            return None, None
        choices = [c for c in self.models.get(re.sub(r'<.*', '', typename).split('.')[-1], [])]
        if len(choices) != 1:
            return None, None
        _, methods = self._class_members(choices[0])
        found = [m for m in methods.get(name, []) if len(named(m, 'parameters').named_children) == arity]
        return (choices[0], found[0]) if len(found) == 1 else (None, None)

    def _lambda(self, node, bound, cls, scope, depth, statuses):
        parameters = named(node, 'parameters')
        names = [text(parameters)] if parameters.type == 'identifier' else [
            text(named(p, 'name')) if named(p, 'name') else text(p) for p in parameters.named_children]
        local = {**scope, **({names[0]: bound} if names and bound is not None and bound[1] is not None else {})}
        body = named(node, 'body')
        if body.type != 'block':
            return self._infer(body, cls, local, depth + 1, statuses)
        results = [self._infer(ret.named_children[0], cls, local, depth + 1, statuses) for ret in _returns(body) if ret.named_children]
        return results[0] if results and all(result == results[0] for result in results) else None

    def _infer(self, node, cls, scope, depth, statuses):
        """('value'|'optional'|'response'|'builder', inner) for one Java expression, or None."""
        try:
            return self._infer_node(node, cls, scope, depth, statuses)
        except (Unsupported, AttributeError, IndexError, TypeError):
            return None

    def _infer_node(self, node, cls, scope, depth, statuses):
        if node is None or depth > 12:
            return None
        kind = node.type
        if kind == 'parenthesized_expression':
            return self._infer(node.named_children[0], cls, scope, depth, statuses)
        if kind in ('identifier', 'field_access'):
            if kind == 'identifier' and not isinstance(scope.get(text(node)), str) and text(node) in scope:
                return scope[text(node)]
            typename = self._receiver_type(node, cls, scope)
            return self._declared(typename) if typename else None
        if kind == 'null_literal':
            return ('value', {'type': 'null'})
        if kind == 'object_creation_expression':
            typename = text(named(node, 'type'))
            body = next((c for c in node.named_children if c.type == 'class_body'), None)
            if re.sub(r'<.*', '', typename) in ('HashMap', 'LinkedHashMap', 'TreeMap'):
                if body is None:
                    return None
                props = {}
                for call in walk(body, 'method_invocation'):
                    args = named(call, 'arguments').named_children
                    if text(named(call, 'name')) != 'put' or named(call, 'object') not in (None,) or len(args) != 2:
                        continue
                    if args[0].type != 'string_literal':
                        return None
                    inner = self._infer(args[1], cls, scope, depth + 1, statuses)
                    if inner is None or inner[0] != 'value' or inner[1] is None:
                        return None
                    props[literal(args[0])] = inner[1]
                return ('value', {'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False})
            return None if body is not None else self._declared(typename)
        if kind == 'method_reference':
            return None
        if kind != 'method_invocation':
            return None
        receiver, name = named(node, 'object'), text(named(node, 'name'))
        args = named(node, 'arguments').named_children
        if receiver is not None and text(receiver) == 'ResponseEntity':
            if name in ('ok', 'accepted') and len(args) == 1:
                statuses.add(RESPONSE_STATUS[name])
                inner = self._infer(args[0], cls, scope, depth + 1, statuses)
                return ('response', inner) if inner else None
            if name in RESPONSE_STATUS or name == 'status':
                if name == 'status':
                    raw = text(args[0]) if args else ''
                    code = int(raw) if raw.isdigit() else STATUS.get(raw.split('.')[-1])
                    if code is None:
                        return None
                    statuses.add(code)
                else:
                    statuses.add(RESPONSE_STATUS[name])
                return ('builder', None)
            return None
        if receiver is not None and receiver.type == 'method_invocation' and name in ('body', 'build'):
            built = self._infer(receiver, cls, scope, depth + 1, statuses)
            if built is None or built[0] != 'builder':
                return None
            if name == 'build':
                return ('response', ('value', {'type': 'null'}))
            inner = self._infer(args[0], cls, scope, depth + 1, statuses) if len(args) == 1 else None
            return ('response', inner) if inner else None
        if receiver is None or (receiver.type == 'this'):
            target, method = self._call_target(text(named(cls, 'name')), name, len(args))
            return self._method_result(target, method, depth, statuses) if method is not None else None
        typename = self._receiver_type(receiver, cls, scope) if receiver.type in ('identifier', 'field_access') else None
        if typename and not typename.startswith('Optional'):
            target, method = self._call_target(typename, name, len(args))
            if method is not None:
                return self._method_result(target, method, depth, statuses)
        value_ = self._infer(receiver, cls, scope, depth + 1, statuses)
        if value_ is None or value_[0] != 'optional':
            return None
        if name in ('get', 'orElseThrow') and len(args) <= 1:
            return value_[1] if value_[1] and value_[1][1] is not None else None
        if name in ('map', 'flatMap') and len(args) == 1:
            if args[0].type == 'lambda_expression':
                result = self._lambda(args[0], value_[1], cls, scope, depth, statuses)
            elif args[0].type == 'method_reference' and text(args[0]).startswith('this::'):
                target, method = self._call_target(text(named(cls, 'name')), text(args[0]).split('::')[-1], 1)
                result = self._method_result(target, method, depth, statuses) if method is not None else None
            else:
                result = None
            if result is None:
                return None
            return result if name == 'flatMap' else ('optional', result)
        return None

    def _response(self, method, cls):
        """The JSON success body and status of a handler whose declared type does not say it."""
        statuses, scope = set(), self._scope(method)
        results = [self._infer(ret.named_children[0], cls, scope, 0, statuses) for ret in _returns(named(method, 'body'))
                   if ret.named_children]
        bodies = [result[1] for result in results if result and result[0] == 'response' and result[1]
                  and result[1][0] == 'value' and result[1][1] is not None]
        if not results or len(bodies) != len(results) or any(body != bodies[0] for body in bodies) or len(statuses) != 1:
            return None, None
        return bodies[0][1], statuses.pop()

    def _method(self, opid, path, verb, method, attrs, location, controller):
        groups, group_required, paths, queries, headers = {}, [], {}, {}, {}
        has_body, body_required = False, False
        for param in named(method, 'parameters').named_children:
            if param.type != 'formal_parameter':
                raise Unsupported('Only named parameters are supported.')
            ann, typename, parameter_name = annotations(param), text(named(param, 'type')), text(named(param, 'name'))
            if ('AuthenticationPrincipal' in ann or 'CurrentUser' in ann or typename.split('.')[-1] in
                    ('Principal', 'Authentication', 'HttpServletRequest', 'HttpServletResponse', 'HttpSession', 'Model')):
                continue
            if 'Validated' in ann or any(a.type == 'element_value_pair' for a in ann.get('Valid', {}).values()):
                raise Unsupported('Validation groups need an explicit contract.')
            schema = self.schema(typename, validate='Valid' in ann)
            kind = next((key for key in ('PathVariable', 'RequestParam', 'RequestBody', 'RequestHeader') if key in ann), None)
            if kind == 'RequestBody':
                if has_body:
                    raise Unsupported('Only one request body can be bound.')
                has_body, body_required = True, value(ann[kind], 'required', True)
                if self.jackson['unwrap']:
                    # UNWRAP_ROOT_VALUE: Jackson reads {"<root name>": {...}} for every request body.
                    root = self._root_name(typename)
                    schema = object_schema({root: schema}, [root])
                groups['body'] = schema
                if body_required: group_required.append('body')
                continue
            if kind is None:
                if schema.get('type') != 'object':
                    raise Unsupported('Unannotated scalar parameters need explicit binding annotations.')
                props = schema['properties']
                needed = schema['required']
                group = groups.setdefault('query', object_schema({}))
                for key, item in props.items():
                    if key in group['properties']:raise Unsupported('Duplicate query field.')
                    # URI form values cannot encode JSON null. Omitting a field
                    # is the wire representation of an optional nullable property.
                    if 'anyOf' in item and len(item['anyOf']) == 2 and item['anyOf'][1] == {'type': 'null'}:
                        item = item['anyOf'][0]
                    group['properties'][key] = item
                    queries[key] = {'pointer': '/query/' + key, 'required': key in needed, 'explode': True}
                group['required'].extend(needed)
                continue
            options = ann[kind]
            key = value(options, 'name', value(options, default=parameter_name))
            if kind == 'RequestHeader' and key.lower() in ('authorization', 'cookie'):
                continue  # The host credential provider supplies authentication.
            group_name = {'PathVariable': 'path', 'RequestParam': 'query', 'RequestHeader': 'headers'}[kind]
            needed = value(options, 'required', True)
            if 'defaultValue' in options:
                default = value(options, 'defaultValue')
                try:
                    schema['default'] = {'integer': int, 'number': float, 'boolean': lambda v: {'true': True, 'false': False}[v]}.get(schema.get('type'), str)(default)
                except (ValueError, KeyError):
                    raise Unsupported('Invalid literal parameter default.') from None
                needed = False
            group = groups.setdefault(group_name, object_schema({}))
            group['properties'][key] = schema
            if needed:group['required'].append(key)
            if group_name == 'path':paths[key] = '/path/' + key
            elif group_name == 'query':queries[key] = {'pointer': '/query/' + key, 'required': needed, 'explode': True}
            else:headers[key] = {'pointer': '/headers/' + key, 'required': needed}
        for group_name in ('path', 'query', 'headers'):
            if group_name in groups and groups[group_name]['required']:
                group_required.append(group_name)
        returned = text(named(method, 'type'))
        if returned in ('String', 'ResponseEntity<String>'):
            raise Unsupported('Spring String response uses a text codec; return a typed JSON DTO.')
        declared = self._declared(returned)
        if declared is None:
            output, status = self._response(method, controller)
            if output is None:
                output = self.open_output(f'The {returned} body of this handler is not read to a declared JSON type')
                statuses = (200, 201, 202)
            else:
                statuses = (status,)
                if self.jackson['wrap']:
                    raise Unsupported('WRAP_ROOT_VALUE responses need an explicit schema.')
        else:
            try:
                output = self.schema(returned, output=True)
            except Unsupported as error:
                output = self.open_output(str(error))
            status = 200
            response_status = attrs.get('ResponseStatus')
            # ResponseEntity's return-value handler sets the final status, overriding
            # the method's earlier @ResponseStatus assignment.
            if returned.startswith('ResponseEntity'):
                calls = [n for n in walk(named(method, 'body'), 'method_invocation') if text(named(n, 'object')) == 'ResponseEntity']
                codes = set()
                for call in calls:
                    name = text(named(call, 'name'))
                    if name in ('ok', 'created', 'noContent'):
                        codes.add({'ok': 200, 'created': 201, 'noContent': 204}[name])
                    elif name == 'status':
                        argument = named(call, 'arguments').named_children[0]
                        raw = text(argument);codes.add(int(raw) if raw.isdigit() else STATUS.get(raw.split('.')[-1]))
                if len(codes) != 1:
                    raise Unsupported('ResponseEntity requires one statically known success status.')
                status = codes.pop()
            elif response_status:
                node = response_status.get('code') or response_status.get('value')
                raw = text(node)
                status = int(raw) if raw.isdigit() else STATUS.get(raw.split('.')[-1])
            statuses = (status,)
            if self.jackson['wrap'] and output.get('type') == 'object':
                root = self._root_name(returned)
                output = object_schema({root: output}, [root])
        if self.jackson['code']:
            self.warn('JACKSON_CUSTOMIZED_IN_CODE', 'The ObjectMapper is customized in Java code; check body and field names.')
        summary = value(attrs.get('Operation', {}), 'summary', opid)
        return record(self.namespace, opid, path, verb, object_schema(groups, group_required), output, location,
                      title=summary, statuses=statuses, path_bindings=paths, query_bindings=queries,
                      header_bindings=headers, body=has_body, body_required=body_required)
