"""Static Spring MVC route and local Java DTO extraction, without OpenAPI."""

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


class SpringSourceImporter(SourceImporter):
    language, extension = 'java', '.java'

    def _extract(self):
        self.models = {}
        has_advice = any(n.type in ('annotation', 'marker_annotation') and text(named(n, 'name')).split('.')[-1]
                         in ('RestControllerAdvice', 'ControllerAdvice') for _, unit in self.units for n in walk(unit))
        for path, unit in self.units:
            for node in walk(unit):
                if node.type in ('class_declaration', 'record_declaration', 'enum_declaration'):
                    self.models.setdefault(text(named(node, 'name')), []).append(node)
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
                        if has_advice:raise Unsupported('Global controller advice requires an explicit response/exception contract.')
                        if len(mappings) != 1:
                            raise Unsupported('Multiple method mappings require explicit selection.')
                        mapping = mappings[0]
                        options = attrs[mapping]
                        if {'params', 'headers'} & (base.keys() | options.keys()):
                            raise Unsupported('Conditional request mapping needs an explicit binding.')
                        prefix = value(base, 'path', value(base, default='')) or ''
                        suffix = value(options, 'path', value(options, default='')) or ''
                        route = (prefix.rstrip('/') + ('/' + suffix.lstrip('/') if suffix else '')) or '/'
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
                        yield self._method(opid, route, verb, method, attrs, location)
                    except (Unsupported, AttributeError, TypeError) as error:
                        yield self.unsupported(opid, route, verb, location, str(error) or 'Unsupported mapping syntax.')

    def schema(self, typename, *, stack=(), substitutions=None, validate=False):
        substitutions = substitutions or {}
        typename = substitutions.get(typename.strip(), typename.strip())
        if len(stack) > 32 or typename in stack:
            raise Unsupported('Recursive/deep DTOs need an explicit finite wrapper.')
        if typename.endswith('[]'):
            return {'type': 'array', 'items': self.schema(typename[:-2], stack=stack)}
        match = re.fullmatch(r'([\w.]+)(?:<(.*)>)?', typename)
        if not match:
            raise Unsupported('Unsupported Java type: ' + typename)
        name, arguments = match.groups()
        name = name.split('.')[-1]
        args = split_types(arguments) if arguments else []
        primitives = {'String': 'string', 'char': 'string', 'Character': 'string', 'boolean': 'boolean', 'Boolean': 'boolean',
                      'int': 'integer', 'Integer': 'integer', 'long': 'integer', 'Long': 'integer', 'short': 'integer',
                      'Short': 'integer', 'byte': 'integer', 'Byte': 'integer', 'double': 'number', 'Double': 'number',
                      'float': 'number', 'Float': 'number'}
        if name in primitives:
            return {'type': primitives[name]}
        if name in ('void', 'Void'):
            return {'type': 'null'}
        if name == 'LocalDateTime':
            return {'type': 'string', 'description': 'ISO local date-time without a UTC offset.'}
        if name in ('LocalDate', 'OffsetDateTime', 'Instant'):
            return {'type': 'string', 'format': 'date' if name == 'LocalDate' else 'date-time'}
        if name in ('List', 'Set') and len(args) == 1:
            return {'type': 'array', 'items': self.schema(args[0], stack=stack, substitutions=substitutions, validate=validate)}
        if name == 'ResponseEntity' and len(args) == 1:
            return self.schema(args[0], stack=stack, validate=validate)
        if name == 'Optional' and len(args) == 1:
            return {'anyOf': [self.schema(args[0], stack=stack, validate=validate), {'type': 'null'}]}
        choices = self.models.get(name, [])
        if len(choices) != 1:
            raise Unsupported('Unresolved or ambiguous Java DTO: ' + name)
        model = choices[0]
        attrs = annotations(model)
        if any(key.startswith('Json') and key not in ('JsonIgnoreProperties',) for key in attrs):
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
        props, required = {}, []
        parent = named(model, 'superclass')
        if parent:
            inherited = self.schema(text(parent.named_children[0]), stack=stack + (typename,), substitutions=substitutions, validate=validate)
            props.update(inherited['properties']); required.extend(inherited['required'])
        fields = named(model, 'parameters').named_children if model.type == 'record_declaration' else named(model, 'body').named_children
        for field in fields:
            if field.type not in ('field_declaration', 'formal_parameter'):
                continue
            modifiers = next((c for c in field.named_children if c.type == 'modifiers'), None)
            if modifiers and any(token in text(modifiers).split() for token in ('static', 'transient')):
                continue
            ann = annotations(field)
            if 'JsonIgnore' in ann and value(ann['JsonIgnore'], default=True):
                continue
            if any(key.startswith('Json') and key not in ('JsonProperty', 'JsonIgnore') for key in ann):
                raise Unsupported('Custom Jackson field behavior needs an explicit schema.')
            if set(ann.get('JsonProperty', {})) - {'value', 'required'}:
                raise Unsupported('Directional Jackson field behavior needs an explicit contract.')
            type_name = text(named(field, 'type'))
            variables = [c for c in field.named_children if c.type == 'variable_declarator'] if field.type == 'field_declaration' else [field]
            for variable in variables:
                original = text(named(variable, 'name'))
                public_field = modifiers is not None and 'public' in text(modifiers).split()
                getters = {text(named(c, 'name')) for c in named(model, 'body').named_children if c.type == 'method_declaration'}
                if (model.type != 'record_declaration' and not public_field and 'JsonProperty' not in ann
                        and not {'Getter', 'Data'} & attrs.keys()
                        and 'get' + original[:1].upper() + original[1:] not in getters
                        and 'is' + original[:1].upper() + original[1:] not in getters):
                    raise Unsupported('DTO field access needs a public field/getter, record, Lombok Getter/Data or JsonProperty.')
                field_name = value(ann.get('JsonProperty', {}), default=original)
                if field_name in props:
                    raise Unsupported('Shadowed or duplicate JSON fields need an explicit schema.')
                item = self.schema(type_name, stack=stack + (typename,), substitutions=substitutions,
                                   validate=validate and 'Valid' in ann)
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
                # Reference fields can be null; @Valid + non-null constraints close
                # that branch. Primitive fields always have a concrete zero value.
                if (type_name not in ('char', 'boolean', 'int', 'long', 'short', 'byte', 'double', 'float')
                        and not (validate and {'NotNull', 'NotBlank', 'NotEmpty'} & ann.keys())
                        and 'anyOf' not in item):
                    item = {'anyOf': [item, {'type': 'null'}]}
                description = ann.get('Schema', {}).get('description')
                if description and description.type == 'string_literal':
                    item['description'] = literal(description)
                props[field_name] = item
        return object_schema(props, required)

    def _method(self, opid, path, verb, method, attrs, location):
        groups, group_required, paths, queries, headers = {}, [], {}, {}, {}
        has_body, body_required = False, False
        for param in named(method, 'parameters').named_children:
            if param.type != 'formal_parameter':
                raise Unsupported('Only named parameters are supported.')
            ann, typename, parameter_name = annotations(param), text(named(param, 'type')), text(named(param, 'name'))
            if ('AuthenticationPrincipal' in ann or typename.split('.')[-1] in
                    ('Principal', 'Authentication', 'HttpServletRequest', 'HttpServletResponse')):
                continue
            if 'Validated' in ann or any(a.type == 'element_value_pair' for a in ann.get('Valid', {}).values()):
                raise Unsupported('Validation groups need an explicit contract.')
            schema = self.schema(typename, validate='Valid' in ann)
            kind = next((key for key in ('PathVariable', 'RequestParam', 'RequestBody', 'RequestHeader') if key in ann), None)
            if kind == 'RequestBody':
                if has_body:
                    raise Unsupported('Only one request body can be bound.')
                has_body, body_required = True, value(ann[kind], 'required', True)
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
        output = self.schema(text(named(method, 'type')))
        if text(named(method, 'type')) in ('String', 'ResponseEntity<String>'):
            raise Unsupported('Spring String response uses a text codec; return a typed JSON DTO.')
        status = 200
        response_status = attrs.get('ResponseStatus')
        # ResponseEntity's return-value handler sets the final status, overriding
        # the method's earlier @ResponseStatus assignment.
        if text(named(method, 'type')).startswith('ResponseEntity'):
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
        summary = value(attrs.get('Operation', {}), 'summary', opid)
        return record(self.namespace, opid, path, verb, object_schema(groups, group_required), output, location,
                      title=summary, statuses=(status,), path_bindings=paths, query_bindings=queries,
                      header_bindings=headers, body=has_body, body_required=body_required)
