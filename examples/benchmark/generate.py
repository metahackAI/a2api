"""Generate the benchmark API: OpenAPI + Spring Boot + Go net/http + Rust Axum + Python.

python examples/benchmark/generate.py [--out artifacts/benchmark]

Deterministic output per scale under <out>/<scale>/{openapi.json,spring,go,rust,python}.
Generated sources stay inside the existing importer syntax profiles.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

from domain import (DEFAULT_LIMIT, FIXED_TIME, MAX_LIMIT, SCALES, Resource, operations, resources)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def pascal(name):
    return name[:1].upper() + name[1:]


def snake(name):
    return ''.join('_' + c.lower() if c.isupper() else c for c in name).lstrip('_')


def quote(value):
    return json.dumps(value, ensure_ascii=False)


# --------------------------------------------------------------------------- OpenAPI

def field_schema(item, *, nullable=True):
    schema = {'string': {'type': 'string'}, 'integer': {'type': 'integer', 'minimum': 0},
              'boolean': {'type': 'boolean'}, 'strings': {'type': 'array', 'items': {'type': 'string'}}}[item.kind]
    schema = dict(schema)
    if item.enum:
        schema['enum'] = list(item.enum)
    if item.nullable and nullable:
        schema['type'] = [schema['type'], 'null']
    schema['description'] = item.label
    return schema


def openapi(scale):
    ref = lambda name: {'$ref': '#/components/schemas/' + name}
    error = {'description': '오류', 'content': {'application/json': {'schema': ref('Error')}}}
    schemas = {
        'Audit': {'type': 'object', 'required': ['createdBy', 'updatedBy', 'revision', 'source'], 'properties': {
            'createdBy': {'type': 'string'}, 'updatedBy': {'type': 'string'}, 'revision': {'type': 'integer'},
            'source': {'type': 'string'}}},
        'SearchRequest': {'type': 'object', 'required': ['query'], 'additionalProperties': False, 'properties': {
            'query': {'type': 'string', 'minLength': 1, 'description': '검색어'},
            'limit': {'type': 'integer', 'minimum': 1, 'maximum': MAX_LIMIT, 'description': '최대 결과 수'}}},
        'Error': {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    }
    paths = {}
    for resource in resources(scale):
        cls = resource.cls
        schemas[cls] = {'type': 'object', 'required': ['id', *[f.name for f in resource.fields], 'tenantId', 'internalNote', 'audit'],
                        'properties': {'id': {'type': 'string', 'description': resource.label + ' ID'},
                                       **{f.name: field_schema(f) for f in resource.fields},
                                       'tenantId': {'type': 'string'}, 'internalNote': {'type': 'string'}, 'audit': ref('Audit')}}
        schemas[cls + 'Page'] = {'type': 'object', 'required': ['items', 'page', 'limit', 'total', 'hasMore'], 'properties': {
            'items': {'type': 'array', 'items': ref(cls)}, 'page': {'type': 'integer'}, 'limit': {'type': 'integer'},
            'total': {'type': 'integer'}, 'hasMore': {'type': 'boolean'}}}
        if 'create' in resource.ops:
            names = [*resource.create_required, *resource.create_optional]
            schemas['New' + cls] = {'type': 'object', 'required': list(resource.create_required), 'additionalProperties': False,
                                    'properties': {name: field_schema(resource.field(name), nullable=False) for name in names}}
        if 'update' in resource.ops:
            schemas[cls + 'Patch'] = {'type': 'object', 'additionalProperties': False,
                                      'properties': {name: field_schema(resource.field(name), nullable=False) for name in resource.patch}}
        if 'tracking' in resource.ops:
            schemas[cls + 'Tracking'] = {'type': 'object', 'required': ['shipmentId', 'events'], 'properties': {
                'shipmentId': {'type': 'string'}, 'events': {'type': 'array', 'items': {'type': 'object',
                    'required': ['time', 'location', 'description'], 'properties': {
                        'time': {'type': 'string'}, 'location': {'type': 'string'}, 'description': {'type': 'string'}}}}}}
        identifier = {'name': 'id', 'in': 'path', 'required': True, 'schema': {'type': 'string'}, 'description': resource.label + ' ID'}
        for op in resource.ops:
            method, path = resource.route(op)
            operation = {'operationId': resource.operation_id(op), 'summary': resource.summary(op), 'tags': [resource.label]}
            if op == 'list':
                operation['parameters'] = [
                    *({'name': name, 'in': 'query', 'required': False, 'schema': field_schema(resource.field(name), nullable=False)}
                      for name in resource.filters),
                    {'name': 'page', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'minimum': 1, 'default': 1}},
                    {'name': 'limit', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'minimum': 1,
                                                                                    'maximum': MAX_LIMIT, 'default': DEFAULT_LIMIT}}]
                operation['responses'] = {'200': {'description': '페이지', 'content': {'application/json': {'schema': ref(cls + 'Page')}}}, '400': error}
            elif op == 'search':
                operation['requestBody'] = {'required': True, 'content': {'application/json': {'schema': ref('SearchRequest')}}}
                operation['responses'] = {'200': {'description': '검색 결과', 'content': {'application/json': {'schema': ref(cls + 'Page')}}}, '400': error}
            elif op == 'create':
                operation['requestBody'] = {'required': True, 'content': {'application/json': {'schema': ref('New' + cls)}}}
                operation['responses'] = {'201': {'description': '생성됨', 'content': {'application/json': {'schema': ref(cls)}}}, '400': error}
            else:
                operation['parameters'] = [identifier]
                if op == 'update':
                    operation['requestBody'] = {'required': True, 'content': {'application/json': {'schema': ref(cls + 'Patch')}}}
                if op == 'delete':
                    operation['responses'] = {'204': {'description': '삭제됨'}, '404': error}
                elif op == 'tracking':
                    operation['responses'] = {'200': {'description': '추적 이벤트', 'content': {'application/json': {'schema': ref(cls + 'Tracking')}}},
                                              '404': error, '503': error}
                else:
                    operation['responses'] = {'200': {'description': resource.label, 'content': {'application/json': {'schema': ref(cls)}}},
                                              '404': error, **({'400': error} if op == 'update' else {}),
                                              **({'409': error} if op == 'cancel' else {})}
            paths.setdefault(path, {})[method.lower()] = operation
    return {'openapi': '3.1.0', 'info': {'title': 'a2api benchmark commerce API (' + scale + ')', 'version': '1.0.0',
                                          'description': '고객·주문·배송·지원 티켓과 업무 리소스를 다루는 합성 API'},
            'servers': [{'url': 'http://127.0.0.1'}], 'paths': paths, 'components': {'schemas': schemas}}


# --------------------------------------------------------------------------- Java / Spring

def java_type(resource, item, *, boxed=False):
    if item.enum:
        return resource.cls + pascal(item.name)
    if item.kind == 'integer':
        return 'Integer' if boxed else 'int'
    if item.kind == 'boolean':
        return 'Boolean' if boxed else 'boolean'
    if item.kind == 'strings':
        return 'List<String>'
    return 'String'


def java_literal(resource, item, value):
    if value is None:
        return 'null'
    if item.enum:
        return java_type(resource, item) + '.' + value
    if item.kind == 'strings':
        return 'new ArrayList<>(List.of(' + ', '.join(quote(v) for v in value) + '))'
    if item.kind == 'boolean':
        return 'true' if value else 'false'
    return str(value) if item.kind == 'integer' else quote(value)


def java_format(resource):
    return resource.id_format.replace('{:', '%').replace('d}', 'd')


def spring(scale, root):
    package = root / 'src/main/java/bench'
    package.mkdir(parents=True)
    (root / 'pom.xml').write_text(f'''<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-parent</artifactId><version>4.0.0</version></parent>
  <groupId>bench</groupId><artifactId>bench-{scale}</artifactId><version>1.0.0</version>
  <properties><java.version>25</java.version><project.build.sourceEncoding>UTF-8</project.build.sourceEncoding></properties>
  <dependencies>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-webmvc</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
  </dependencies>
  <build><plugins><plugin><groupId>org.springframework.boot</groupId><artifactId>spring-boot-maven-plugin</artifactId></plugin></plugins></build>
</project>
''')
    imports = '''import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
'''
    (package / 'App.java').write_text('''package bench;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class App {
    public static void main(String[] args) { SpringApplication.run(App.class, args); }
}
''')
    (package / 'Common.java').write_text(f'''package bench;

{imports}
record Audit(String createdBy, String updatedBy, int revision, String source) {{
    static Audit seeded() {{ return new Audit("seed", "seed", 1, "migration"); }}
    static Audit created() {{ return new Audit("api", "api", 1, "api"); }}
    Audit next() {{ return new Audit(createdBy, "api", revision + 1, source); }}
}}

record SearchRequest(@NotBlank String query, Integer limit) {{}}

record TrackingEvent(String time, String location, String description) {{}}

final class Paging {{
    static final int DEFAULT_LIMIT = {DEFAULT_LIMIT};
    static final int MAX_LIMIT = {MAX_LIMIT};

    static int[] bounds(Integer page, Integer limit) {{
        int p = page == null ? 1 : page;
        int l = limit == null ? DEFAULT_LIMIT : limit;
        if (p < 1 || l < 1) throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "page and limit must be positive");
        return new int[] {{p, Math.min(l, MAX_LIMIT)}};
    }}

    static <T> List<T> slice(List<T> rows, int[] bounds) {{
        int from = Math.min((bounds[0] - 1) * bounds[1], rows.size());
        return new ArrayList<>(rows.subList(from, Math.min(from + bounds[1], rows.size())));
    }}

    static boolean contains(Object value, String needle) {{
        return value != null && String.valueOf(value).toLowerCase().contains(needle.toLowerCase());
    }}

    static void nonnegative(Integer value) {{
        if (value != null && value < 0) throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "negative value");
    }}

    static ResponseStatusException missing() {{ return new ResponseStatusException(HttpStatus.NOT_FOUND, "not found"); }}
}}
''')
    store_fields, seeds = [], []
    for resource in resources(scale):
        store_fields.append(f'    final Map<String, {resource.cls}> {resource.key} = new LinkedHashMap<>();\n    int {resource.key}Next;')
        seeds.append(f'        {resource.key}.clear();\n        {resource.key}Next = {resource.next_number()};')
        for row in resource.seeds:
            args = [quote(row['id'])] + [java_literal(resource, item, row[item.name]) for item in resource.fields]
            args += ['"tenant-a"', quote('server-only note for ' + row['id']), 'Audit.seeded()']
            seeds.append(f'        {resource.key}.put({quote(row["id"])}, new {resource.cls}({", ".join(args)}));')
    (package / 'Store.java').write_text(f'''package bench;

{imports}import org.springframework.stereotype.Component;

@Component
class Store {{
    static final String FIXED_TIME = {quote(FIXED_TIME)};
    static final boolean TRACKING_AVAILABLE = false;
{chr(10).join(store_fields)}

    Store() {{ reset(); }}

    synchronized void reset() {{
{chr(10).join(seeds)}
    }}
}}
''')
    state_components = ', '.join(f'List<{r.cls}> {r.key}' for r in resources(scale))
    state_values = ', '.join(f'new ArrayList<>(store.{r.key}.values())' for r in resources(scale))
    (package / 'AdminController.java').write_text(f'''package bench;

{imports}
record Snapshot({state_components}) {{}}

@RestController
@RequestMapping("/__admin")
public class AdminController {{
    private final Store store;

    public AdminController(Store store) {{ this.store = store; }}

    @PostMapping("/reset")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void reset() {{ store.reset(); }}

    @GetMapping("/state")
    public Snapshot state() {{
        synchronized (store) {{ return new Snapshot({state_values}); }}
    }}
}}
''')
    for resource in resources(scale):
        (package / (resource.cls + 'Controller.java')).write_text(spring_controller(resource, imports))


def spring_controller(r: Resource, imports):
    cls, key = r.cls, r.key
    lines = [f'package bench;\n\n{imports}']
    for item in r.fields:
        if item.enum:
            lines.append(f'enum {cls}{pascal(item.name)} {{ {", ".join(item.enum)} }}\n')
    components = ', '.join([f'String id'] + [f'{java_type(r, f)} {f.name}' for f in r.fields]
                           + ['String tenantId', 'String internalNote', 'Audit audit'])
    lines.append(f'record {cls}({components}) {{}}\n')
    lines.append(f'record {cls}Page(List<{cls}> items, int page, int limit, int total, boolean hasMore) {{}}\n')
    if 'create' in r.ops:
        parts = []
        for name in r.create_required:
            item = r.field(name)
            if item.kind == 'string' and not item.enum:
                parts.append(f'@NotBlank String {name}')
            elif item.kind == 'integer':
                parts.append(f'@NotNull @Min(0) Integer {name}')
            else:
                parts.append(f'@NotNull {java_type(r, item, boxed=True)} {name}')
        parts += [f'{java_type(r, r.field(name), boxed=True)} {name}' for name in r.create_optional]
        lines.append(f'record New{cls}({", ".join(parts)}) {{}}\n')
    if 'update' in r.ops:
        parts = [f'{java_type(r, r.field(name), boxed=True)} {name}' for name in r.patch]
        lines.append(f'record {cls}Patch({", ".join(parts)}) {{}}\n')
    if 'tracking' in r.ops:
        lines.append(f'record {cls}Tracking(String shipmentId, List<TrackingEvent> events) {{}}\n')
    body = []
    body.append(f'''    private final Store store;

    public {cls}Controller(Store store) {{ this.store = store; }}

    private {cls} require(String id) {{
        {cls} row = store.{key}.get(id);
        if (row == null) throw Paging.missing();
        return row;
    }}
''')

    def rebuild(changes, audit='old.audit().next()'):
        values = ['old.id()'] + [changes.get(f.name, f'old.{f.name}()') for f in r.fields]
        values += ['old.tenantId()', 'old.internalNote()', audit]
        return f'new {cls}({", ".join(values)})'

    for op in r.ops:
        if op == 'list':
            params, filters = [], []
            for name in r.filters:
                item = r.field(name)
                params.append(f'@RequestParam(required = false) {java_type(r, item, boxed=True)} {name}')
                if item.enum or item.kind == 'boolean':
                    filters.append(f'.filter(row -> {name} == null || row.{name}() == {name})')
                else:
                    filters.append(f'.filter(row -> {name} == null || {name}.isEmpty() || {name}.equals(row.{name}()))')
            params += ['@RequestParam(required = false) Integer page', '@RequestParam(required = false) Integer limit']
            body.append(f'''    @GetMapping
    public {cls}Page list({", ".join(params)}) {{
        int[] bounds = Paging.bounds(page, limit);
        synchronized (store) {{
            List<{cls}> rows = store.{key}.values().stream()
                {chr(10).join("                " + f for f in filters).strip()}
                .toList();
            return new {cls}Page(Paging.slice(rows, bounds), bounds[0], bounds[1], rows.size(), bounds[0] * bounds[1] < rows.size());
        }}
    }}
''')
        elif op == 'get':
            body.append(f'''    @GetMapping("/{{id}}")
    public {cls} get(@PathVariable String id) {{
        synchronized (store) {{ return require(id); }}
    }}
''')
        elif op == 'create':
            values = []
            for item in r.fields:
                if item.name in r.create_required:
                    values.append(f'body.{item.name}()')
                elif item.name in r.create_optional:
                    values.append(f'body.{item.name}() == null ? {java_literal(r, item, r.create_defaults[item.name])} : body.{item.name}()')
                elif item.name == 'createdAt':
                    values.append('Store.FIXED_TIME')
                else:
                    values.append(java_literal(r, item, r.create_defaults.get(item.name)))
            checks = ''.join(f'        Paging.nonnegative(body.{n}());\n' for n in r.create_required if r.field(n).kind == 'integer')
            body.append(f'''    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public {cls} create(@RequestBody @Valid New{cls} body) {{
{checks}        synchronized (store) {{
            String id = String.format("{java_format(r)}", store.{key}Next++);
            {cls} row = new {cls}(id, {", ".join(values)}, "tenant-a", "server-only note for " + id, Audit.created());
            store.{key}.put(id, row);
            return row;
        }}
    }}
''')
        elif op == 'update':
            changes = {name: f'body.{name}() != null ? body.{name}() : old.{name}()' for name in r.patch}
            checks = ''.join(f'        Paging.nonnegative(body.{n}());\n' for n in r.patch if r.field(n).kind == 'integer')
            body.append(f'''    @PatchMapping("/{{id}}")
    public {cls} update(@PathVariable String id, @RequestBody {cls}Patch body) {{
{checks}        synchronized (store) {{
            {cls} old = require(id);
            {cls} row = {rebuild(changes)};
            store.{key}.put(id, row);
            return row;
        }}
    }}
''')
        elif op == 'delete':
            body.append(f'''    @DeleteMapping("/{{id}}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable String id) {{
        synchronized (store) {{ require(id); store.{key}.remove(id); }}
    }}
''')
        elif op == 'search':
            condition = ' || '.join(f'Paging.contains(row.{name}(), body.query())' for name in r.search)
            body.append(f'''    @PostMapping("/search")
    public {cls}Page search(@RequestBody @Valid SearchRequest body) {{
        int[] bounds = Paging.bounds(1, body.limit());
        synchronized (store) {{
            List<{cls}> rows = store.{key}.values().stream().filter(row -> {condition}).toList();
            return new {cls}Page(Paging.slice(rows, bounds), 1, bounds[1], rows.size(), bounds[1] < rows.size());
        }}
    }}
''')
        elif op == 'cancel':
            status_type = cls + 'Status'
            body.append(f'''    @PostMapping("/{{id}}/cancel")
    public {cls} cancel(@PathVariable String id) {{
        synchronized (store) {{
            {cls} old = require(id);
            if (old.status() != {status_type}.pending && old.status() != {status_type}.paid) {{
                throw new ResponseStatusException(HttpStatus.CONFLICT, "only pending or paid orders can be cancelled");
            }}
            {cls} row = {rebuild({"status": status_type + ".cancelled"})};
            store.{key}.put(id, row);
            return row;
        }}
    }}
''')
        elif op == 'tracking':
            body.append(f'''    @GetMapping("/{{id}}/tracking")
    public {cls}Tracking tracking(@PathVariable String id) {{
        synchronized (store) {{ require(id); }}
        if (!Store.TRACKING_AVAILABLE) {{
            throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE, "carrier tracking service unavailable");
        }}
        return new {cls}Tracking(id, List.of());
    }}
''')
    lines.append(f'@RestController\n@RequestMapping("{r.path}")\npublic class {cls}Controller {{\n' + '\n'.join(body) + '}\n')
    return '\n'.join(lines)


# --------------------------------------------------------------------------- Go

def go_name(name):
    special = {'id': 'ID'}
    if name in special:
        return special[name]
    result = pascal(name)
    return result.replace('Ids', 'IDs').replace('Id', 'ID') if result.endswith(('Id', 'Ids')) else result


def go_type(item, *, pointer=False):
    base = {'string': 'string', 'integer': 'int', 'boolean': 'bool', 'strings': '[]string'}[item.kind]
    return '*' + base if (pointer or item.nullable) and item.kind != 'strings' else base


def go_literal(item, value):
    if value is None:
        return 'nil'
    if item.kind == 'strings':
        return '[]string{' + ', '.join(quote(v) for v in value) + '}'
    if item.kind == 'boolean':
        return 'true' if value else 'false'
    if item.kind == 'integer':
        return str(value)
    return f'ptr({quote(value)})' if item.nullable else quote(value)


def go(scale, root):
    root.mkdir(parents=True)
    (root / 'go.mod').write_text('module example.com/a2api-bench\n\ngo 1.22\n')
    (root / 'common.go').write_text(f'''package main

import (
    "net/http"
    "strconv"
    "strings"
)

const fixedTime = {quote(FIXED_TIME)}
const trackingAvailable = false

type Audit struct {{
    CreatedBy string `json:"createdBy"`
    UpdatedBy string `json:"updatedBy"`
    Revision int `json:"revision"`
    Source string `json:"source"`
}}

type SearchRequest struct {{
    Query string `json:"query"`
    Limit *int `json:"limit"`
}}

type TrackingEvent struct {{
    Time string `json:"time"`
    Location string `json:"location"`
    Description string `json:"description"`
}}

func seededAudit() Audit {{ return Audit{{CreatedBy: "seed", UpdatedBy: "seed", Revision: 1, Source: "migration"}} }}
func createdAudit() Audit {{ return Audit{{CreatedBy: "api", UpdatedBy: "api", Revision: 1, Source: "api"}} }}
func nextAudit(audit Audit) Audit {{ audit.UpdatedBy = "api"; audit.Revision++; return audit }}
func ptr(value string) *string {{ return &value }}

func bounds(rawPage, rawLimit string) (int, int, bool) {{
    page, limit := 1, {DEFAULT_LIMIT}
    var err error
    if rawPage != "" {{
        if page, err = strconv.Atoi(rawPage); err != nil || page < 1 {{ return 0, 0, false }}
    }}
    if rawLimit != "" {{
        if limit, err = strconv.Atoi(rawLimit); err != nil || limit < 1 {{ return 0, 0, false }}
    }}
    if limit > {MAX_LIMIT} {{ limit = {MAX_LIMIT} }}
    return page, limit, true
}}

func searchLimit(value *int) (int, bool) {{
    if value == nil {{ return {DEFAULT_LIMIT}, true }}
    if *value < 1 {{ return 0, false }}
    if *value > {MAX_LIMIT} {{ return {MAX_LIMIT}, true }}
    return *value, true
}}

func pageOf[T any](rows []T, page, limit int) ([]T, bool) {{
    start := (page - 1) * limit
    if start > len(rows) {{ start = len(rows) }}
    end := start + limit
    if end > len(rows) {{ end = len(rows) }}
    return append([]T{{}}, rows[start:end]...), page*limit < len(rows)
}}

func oneOf(value string, choices ...string) bool {{
    for _, choice := range choices {{
        if value == choice {{ return true }}
    }}
    return false
}}

func optionalOneOf(value string, choices ...string) bool {{ return value == "" || oneOf(value, choices...) }}
func validBool(value string) bool {{ return value == "" || value == "true" || value == "false" }}
func contains(value, needle string) bool {{ return strings.Contains(strings.ToLower(value), strings.ToLower(needle)) }}
func badRequest(w http.ResponseWriter, message string) {{ http.Error(w, message, http.StatusBadRequest) }}
''')
    variables, seeds, state_fields, state_values = [], [], [], []
    for r in resources(scale):
        variables.append(f'var {r.key} []{r.cls}\nvar next{r.plural} int')
        rows = []
        for row in r.seeds:
            values = [f'ID: {quote(row["id"])}'] + [f'{go_name(f.name)}: {go_literal(f, row[f.name])}' for f in r.fields]
            values += ['TenantID: "tenant-a"', f'InternalNote: {quote("server-only note for " + row["id"])}', 'Audit: seededAudit()']
            rows.append('        {' + ', '.join(values) + '},')
        seeds.append(f'    {r.key} = []{r.cls}{{\n' + '\n'.join(rows) + f'\n    }}\n    next{r.plural} = {r.next_number()}')
        state_fields.append(f'    {r.plural} []{r.cls} `json:"{r.key}"`')
        state_values.append(f'{r.plural}: {r.key}')
    (root / 'store.go').write_text(f'''package main

import (
    "encoding/json"
    "net/http"
    "sync"
)

var mu sync.Mutex
{chr(10).join(variables)}

type Snapshot struct {{
{chr(10).join(state_fields)}
}}

func seed() {{
{chr(10).join(seeds)}
}}

func resetState(w http.ResponseWriter, r *http.Request) {{
    mu.Lock()
    defer mu.Unlock()
    seed()
    w.WriteHeader(http.StatusNoContent)
}}

func getState(w http.ResponseWriter, r *http.Request) {{
    mu.Lock()
    defer mu.Unlock()
    out := Snapshot{{{", ".join(state_values)}}}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(out)
}}
''')
    registrations = ['    mux.HandleFunc("POST /__admin/reset", resetState)', '    mux.HandleFunc("GET /__admin/state", getState)']
    for r, op in operations(scale):
        method, path = r.route(op)
        registrations.append(f'    mux.HandleFunc("{method} {path}", {r.operation_id(op)})')
    (root / 'main.go').write_text(f'''package main

import (
    "net/http"
    "os"
)

func main() {{
    seed()
    mux := http.NewServeMux()
{chr(10).join(registrations)}
    if err := http.ListenAndServe("127.0.0.1:"+os.Args[1], mux); err != nil {{ panic(err) }}
}}
''')
    for r in resources(scale):
        (root / (r.key + '.go')).write_text(go_resource(r))


def go_resource(r: Resource):
    cls, key = r.cls, r.key
    def struct(name, fields):
        return f'type {name} struct {{\n' + '\n'.join(f'    {a} {b} `json:"{c}"`' for a, b, c in fields) + '\n}\n'
    out = ['package main\n\nimport (\n    "encoding/json"\n    "fmt"\n    "net/http"\n    "strconv"\n)\n\nvar _ = fmt.Sprintf\nvar _ = strconv.Itoa\n']
    out.append(struct(cls, [('ID', 'string', 'id')] + [(go_name(f.name), go_type(f), f.name) for f in r.fields]
                      + [('TenantID', 'string', 'tenantId'), ('InternalNote', 'string', 'internalNote'), ('Audit', 'Audit', 'audit')]))
    out.append(struct(cls + 'Page', [('Items', '[]' + cls, 'items'), ('Page', 'int', 'page'), ('Limit', 'int', 'limit'),
                                     ('Total', 'int', 'total'), ('HasMore', 'bool', 'hasMore')]))
    if 'create' in r.ops:
        fields = []
        for name in r.create_required:
            item = r.field(name)
            fields.append((go_name(name), '*int' if item.kind == 'integer' else go_type(item), name))
        fields += [(go_name(n), go_type(r.field(n), pointer=True), n) for n in r.create_optional]
        out.append(struct('New' + cls, fields))
    if 'update' in r.ops:
        out.append(struct(cls + 'Patch', [(go_name(n), go_type(r.field(n), pointer=True), n) for n in r.patch]))
    if 'tracking' in r.ops:
        out.append(struct(cls + 'Tracking', [('ShipmentID', 'string', 'shipmentId'), ('Events', '[]TrackingEvent', 'events')]))
    out.append(f'''func find{cls}(id string) int {{
    for index, row := range {key} {{
        if row.ID == id {{ return index }}
    }}
    return -1
}}
''')

    def enum_check(name, expression):
        item = r.field(name)
        return f'!optionalOneOf({expression}, {", ".join(quote(v) for v in item.enum)})' if item.enum else None

    def emit(name, extra, status=None):
        status_line = f'    w.WriteHeader(http.{status})\n' if status else ''
        return (f'    w.Header().Set("Content-Type", "application/json")\n{status_line}'
                f'    json.NewEncoder(w).Encode(out)\n')

    for op in r.ops:
        name = r.operation_id(op)
        head = f'func {name}(w http.ResponseWriter, r *http.Request) {{\n    mu.Lock()\n    defer mu.Unlock()\n'
        if op == 'list':
            reads, invalid, conditions = [], [], []
            for field_name in r.filters:
                item = r.field(field_name)
                reads.append(f'    {field_name} := r.URL.Query().Get("{field_name}")')
                if item.kind == 'boolean':
                    invalid.append(f'!validBool({field_name})')
                    conditions.append(f'({field_name} == "" || strconv.FormatBool(row.{go_name(field_name)}) == {field_name})')
                else:
                    check = enum_check(field_name, field_name)
                    if check:
                        invalid.append(check)
                    conditions.append(f'({field_name} == "" || row.{go_name(field_name)} == {field_name})')
            reads.append('    page, limit, ok := bounds(r.URL.Query().Get("page"), r.URL.Query().Get("limit"))')
            invalid = ['!ok'] + invalid
            out.append(head + '\n'.join(reads) + f'''
    if {" || ".join(invalid)} {{
        badRequest(w, "invalid filter, page or limit")
        return
    }}
    matched := []{cls}{{}}
    for _, row := range {key} {{
        if {" && ".join(conditions)} {{
            matched = append(matched, row)
        }}
    }}
    items, hasMore := pageOf(matched, page, limit)
    out := {cls}Page{{Items: items, Page: page, Limit: limit, Total: len(matched), HasMore: hasMore}}
{emit(name, None)}}}
''')
        elif op == 'get':
            out.append(head + f'''    index := find{cls}(r.PathValue("id"))
    if index < 0 {{
        http.NotFound(w, r)
        return
    }}
    var out {cls}
    out = {key}[index]
{emit(name, None)}}}
''')
        elif op == 'create':
            checks = []
            for field_name in r.create_required:
                item = r.field(field_name)
                if item.kind == 'integer':
                    checks.append(f'input.{go_name(field_name)} == nil || *input.{go_name(field_name)} < 0')
                elif item.enum:
                    checks.append(f'!oneOf(input.{go_name(field_name)}, {", ".join(quote(v) for v in item.enum)})')
                else:
                    checks.append(f'input.{go_name(field_name)} == ""')
            optional = []
            for field_name in r.create_optional:
                item = r.field(field_name)
                default = r.create_defaults[field_name]
                optional.append(f'    {field_name} := {quote(default)}\n    if input.{go_name(field_name)} != nil {{ {field_name} = *input.{go_name(field_name)} }}')
                check = enum_check(field_name, field_name)
                if check:
                    checks.append(check)
            values = []
            for item in r.fields:
                if item.name in r.create_required:
                    values.append(f'{go_name(item.name)}: ' + (f'*input.{go_name(item.name)}' if item.kind == 'integer' else f'input.{go_name(item.name)}'))
                elif item.name in r.create_optional:
                    values.append(f'{go_name(item.name)}: {item.name}')
                elif item.name == 'createdAt':
                    values.append(f'{go_name(item.name)}: fixedTime')
                else:
                    default = r.create_defaults.get(item.name)
                    if item.kind == 'strings':
                        values.append(f'{go_name(item.name)}: []string{{}}')
                    elif default is not None:
                        values.append(f'{go_name(item.name)}: {go_literal(item, default)}')
            fmt_spec = r.id_format.replace('{:', '%').replace('d}', 'd')
            out.append(head + f'''    var input New{cls}
    if json.NewDecoder(r.Body).Decode(&input) != nil {{
        badRequest(w, "invalid JSON body")
        return
    }}
{chr(10).join(optional)}
    if {" || ".join(checks)} {{
        badRequest(w, "missing or invalid fields")
        return
    }}
    id := fmt.Sprintf("{fmt_spec}", next{r.plural})
    next{r.plural}++
    out := {cls}{{ID: id, {", ".join(values)}, TenantID: "tenant-a", InternalNote: "server-only note for " + id, Audit: createdAudit()}}
    {key} = append({key}, out)
{emit(name, None, 'StatusCreated')}}}
''')
        elif op == 'update':
            checks, apply = [], []
            for field_name in r.patch:
                item = r.field(field_name)
                go_field = go_name(field_name)
                if item.enum:
                    checks.append(f'(input.{go_field} != nil && !oneOf(*input.{go_field}, {", ".join(quote(v) for v in item.enum)}))')
                if item.kind == 'integer':
                    checks.append(f'(input.{go_field} != nil && *input.{go_field} < 0)')
                if item.nullable:
                    apply.append(f'    if input.{go_field} != nil {{ out.{go_field} = input.{go_field} }}')
                else:
                    apply.append(f'    if input.{go_field} != nil {{ out.{go_field} = *input.{go_field} }}')
            out.append(head + f'''    var input {cls}Patch
    if json.NewDecoder(r.Body).Decode(&input) != nil{"".join(" || " + c for c in checks)} {{
        badRequest(w, "invalid fields")
        return
    }}
    index := find{cls}(r.PathValue("id"))
    if index < 0 {{
        http.NotFound(w, r)
        return
    }}
    var out {cls}
    out = {key}[index]
{chr(10).join(apply)}
    out.Audit = nextAudit(out.Audit)
    {key}[index] = out
{emit(name, None)}}}
''')
        elif op == 'delete':
            out.append(head + f'''    index := find{cls}(r.PathValue("id"))
    if index < 0 {{
        http.NotFound(w, r)
        return
    }}
    {key} = append({key}[:index], {key}[index+1:]...)
    w.WriteHeader(http.StatusNoContent)
}}
''')
        elif op == 'search':
            condition = ' || '.join(f'contains(row.{go_name(n)}, input.Query)' for n in r.search)
            out.append(head + f'''    var input SearchRequest
    if json.NewDecoder(r.Body).Decode(&input) != nil || input.Query == "" {{
        badRequest(w, "query is required")
        return
    }}
    limit, ok := searchLimit(input.Limit)
    if !ok {{
        badRequest(w, "invalid limit")
        return
    }}
    matched := []{cls}{{}}
    for _, row := range {key} {{
        if {condition} {{
            matched = append(matched, row)
        }}
    }}
    items, hasMore := pageOf(matched, 1, limit)
    out := {cls}Page{{Items: items, Page: 1, Limit: limit, Total: len(matched), HasMore: hasMore}}
{emit(name, None)}}}
''')
        elif op == 'cancel':
            out.append(head + f'''    index := find{cls}(r.PathValue("id"))
    if index < 0 {{
        http.NotFound(w, r)
        return
    }}
    var out {cls}
    out = {key}[index]
    if out.Status != "pending" && out.Status != "paid" {{
        http.Error(w, "only pending or paid orders can be cancelled", http.StatusConflict)
        return
    }}
    out.Status = "cancelled"
    out.Audit = nextAudit(out.Audit)
    {key}[index] = out
{emit(name, None)}}}
''')
        elif op == 'tracking':
            out.append(head + f'''    id := r.PathValue("id")
    if find{cls}(id) < 0 {{
        http.NotFound(w, r)
        return
    }}
    if !trackingAvailable {{
        http.Error(w, "carrier tracking service unavailable", http.StatusServiceUnavailable)
        return
    }}
    out := {cls}Tracking{{ShipmentID: id, Events: []TrackingEvent{{}}}}
{emit(name, None)}}}
''')
    return '\n'.join(out)


# --------------------------------------------------------------------------- Rust

def rust_type(item, *, option=False):
    base = {'string': 'String', 'integer': 'i64', 'boolean': 'bool', 'strings': 'Vec<String>'}[item.kind]
    return f'Option<{base}>' if option or item.nullable else base


def rust_literal(item, value):
    if value is None:
        return 'None'
    if item.kind == 'strings':
        return 'vec![' + ', '.join(quote(v) + '.into()' for v in value) + ']'
    if item.kind == 'boolean':
        return 'true' if value else 'false'
    if item.kind == 'integer':
        return str(value)
    return f'Some({quote(value)}.into())' if item.nullable else quote(value) + '.into()'


def rust(scale, root):
    (root / 'src').mkdir(parents=True)
    (root / 'Cargo.toml').write_text(f'''[package]
name = "a2api-bench-{scale}"
version = "1.0.0"
edition = "2021"

[dependencies]
axum = "=0.8.6"
serde = {{ version = "1", features = ["derive"] }}
tokio = {{ version = "1", features = ["macros", "rt-multi-thread", "net"] }}
''')
    lock = REPO / 'examples/source-http/rust/Cargo.lock'
    (root / 'Cargo.lock').write_text(lock.read_text().replace('name = "a2api-source-demo"', f'name = "a2api-bench-{scale}"').replace('version = "0.1.0"\ndependencies = [\n "axum",', 'version = "1.0.0"\ndependencies = [\n "axum",'))
    parts = [f'''#![allow(dead_code)]
use axum::{{extract::{{Json, Path, Query, State}}, http::StatusCode, routing::{{get, post}}, Router}};
use serde::{{Deserialize, Serialize}};
use std::sync::{{Arc, Mutex}};

const FIXED_TIME: &str = {quote(FIXED_TIME)};
const TRACKING_AVAILABLE: bool = false;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct Audit {{ created_by: String, updated_by: String, revision: i64, source: String }}

impl Audit {{
    fn seeded() -> Audit {{ Audit {{ created_by: "seed".into(), updated_by: "seed".into(), revision: 1, source: "migration".into() }} }}
    fn created() -> Audit {{ Audit {{ created_by: "api".into(), updated_by: "api".into(), revision: 1, source: "api".into() }} }}
    fn next(&self) -> Audit {{ Audit {{ created_by: self.created_by.clone(), updated_by: "api".into(), revision: self.revision + 1, source: self.source.clone() }} }}
}}

#[derive(Deserialize)]
struct SearchRequest {{ query: String, limit: Option<u32> }}

#[derive(Clone, Serialize)]
struct TrackingEvent {{ time: String, location: String, description: String }}

fn bounds(page: Option<u32>, limit: Option<u32>) -> Result<(u32, u32), StatusCode> {{
    let page = page.unwrap_or(1);
    let limit = limit.unwrap_or({DEFAULT_LIMIT});
    if page < 1 || limit < 1 {{ return Err(StatusCode::BAD_REQUEST); }}
    Ok((page, limit.min({MAX_LIMIT})))
}}

fn page_of<T: Clone>(rows: &[T], page: u32, limit: u32) -> (Vec<T>, bool) {{
    let start = (((page - 1) * limit) as usize).min(rows.len());
    let end = (start + limit as usize).min(rows.len());
    (rows[start..end].to_vec(), ((page * limit) as usize) < rows.len())
}}

fn one_of(value: &Option<String>, choices: &[&str]) -> Result<(), StatusCode> {{
    match value {{ Some(v) if !v.is_empty() && !choices.contains(&v.as_str()) => Err(StatusCode::BAD_REQUEST), _ => Ok(()) }}
}}

fn nonempty(value: &str) -> Result<(), StatusCode> {{
    if value.is_empty() {{ Err(StatusCode::BAD_REQUEST) }} else {{ Ok(()) }}
}}

fn nonnegative(value: Option<i64>) -> Result<(), StatusCode> {{
    if value.map_or(false, |v| v < 0) {{ Err(StatusCode::BAD_REQUEST) }} else {{ Ok(()) }}
}}

fn contains(value: &str, needle: &str) -> bool {{ value.to_lowercase().contains(&needle.to_lowercase()) }}

type Shared = Arc<Mutex<Store>>;
''']
    store_fields, seeds, snapshot_fields, snapshot_values = [], [], [], []
    for r in resources(scale):
        store_fields.append(f'    {r.key}: Vec<{r.cls}>,\n    next_{r.key}: u32,')
        rows = []
        for row in r.seeds:
            values = [f'id: {quote(row["id"])}.into()'] + [f'{snake(f.name)}: {rust_literal(f, row[f.name])}' for f in r.fields]
            values += ['tenant_id: "tenant-a".into()', f'internal_note: {quote("server-only note for " + row["id"])}.into()', 'audit: Audit::seeded()']
            rows.append(f'            {r.cls} {{ {", ".join(values)} }},')
        seeds.append(f'        {r.key}: vec![\n' + '\n'.join(rows) + f'\n        ],\n        next_{r.key}: {r.next_number()},')
        snapshot_fields.append(f'    {r.key}: Vec<{r.cls}>,')
        snapshot_values.append(f'{r.key}: store.{r.key}.clone()')
        parts.append(rust_resource(r))
    parts.append(f'''struct Store {{
{chr(10).join(store_fields)}
}}

fn seeded() -> Store {{
    Store {{
{chr(10).join(seeds)}
    }}
}}

#[derive(Serialize)]
struct Snapshot {{
{chr(10).join(snapshot_fields)}
}}

async fn reset_state(State(state): State<Shared>) -> StatusCode {{
    *state.lock().unwrap() = seeded();
    StatusCode::NO_CONTENT
}}

async fn get_state(State(state): State<Shared>) -> Json<Snapshot> {{
    let store = state.lock().unwrap();
    Json(Snapshot {{ {", ".join(snapshot_values)} }})
}}
''')
    routes = {}
    for r, op in operations(scale):
        method, path = r.route(op)
        routes.setdefault(path, []).append((method.lower(), r.snake_op(op)))
    chain = ['        .route("/__admin/reset", post(reset_state))', '        .route("/__admin/state", get(get_state))']
    for path, handlers in routes.items():
        first, *rest = handlers
        expression = f'{first[0]}({first[1]})' + ''.join(f'.{m}({h})' for m, h in rest)
        chain.append(f'        .route("{path}", {expression})')
    parts.append(f'''#[tokio::main]
async fn main() {{
    let state = Arc::new(Mutex::new(seeded()));
    let app = Router::new()
{chr(10).join(chain)}
        .with_state(state);
    let port = std::env::args().nth(1).expect("port");
    let listener = tokio::net::TcpListener::bind(format!("127.0.0.1:{{port}}")).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}}
''')
    (root / 'src/main.rs').write_text('\n'.join(parts))


def rust_resource(r: Resource):
    cls, key = r.cls, r.key
    def struct(name, fields, derive='Clone, Serialize'):
        body = ', '.join(f'{snake(n)}: {t}' for n, t in fields)
        return f'#[derive({derive})]\n#[serde(rename_all = "camelCase")]\nstruct {name} {{ {body} }}\n'
    out = [struct(cls, [('id', 'String')] + [(f.name, rust_type(f)) for f in r.fields]
                  + [('tenantId', 'String'), ('internalNote', 'String'), ('audit', 'Audit')]),
           struct(cls + 'Page', [('items', f'Vec<{cls}>'), ('page', 'u32'), ('limit', 'u32'), ('total', 'u32'), ('hasMore', 'bool')])]
    if 'list' in r.ops:
        fields = [(n, 'Option<bool>' if r.field(n).kind == 'boolean' else 'Option<String>') for n in r.filters]
        out.append(struct(cls + 'ListQuery', fields + [('page', 'Option<u32>'), ('limit', 'Option<u32>')], 'Deserialize'))
    if 'create' in r.ops:
        out.append(struct('New' + cls, [(n, rust_type(r.field(n))) for n in r.create_required]
                          + [(n, rust_type(r.field(n), option=True)) for n in r.create_optional], 'Deserialize'))
    if 'update' in r.ops:
        out.append(struct(cls + 'Patch', [(n, rust_type(r.field(n), option=True)) for n in r.patch], 'Deserialize'))
    if 'tracking' in r.ops:
        out.append(struct(cls + 'Tracking', [('shipmentId', 'String'), ('events', 'Vec<TrackingEvent>')]))

    def choices(name):
        return '&[' + ', '.join(quote(v) for v in r.field(name).enum) + ']'

    for op in r.ops:
        fn = r.snake_op(op)
        if op == 'list':
            checks, conditions = [], []
            for name in r.filters:
                item = r.field(name)
                field = snake(name)
                if item.enum:
                    checks.append(f'    one_of(&query.{field}, {choices(name)})?;')
                if item.kind == 'boolean':
                    conditions.append(f'query.{field}.map_or(true, |value| row.{field} == value)')
                else:
                    conditions.append(f'query.{field}.as_ref().filter(|value| !value.is_empty()).map_or(true, |value| &row.{field} == value)')
            out.append(f'''async fn {fn}(State(state): State<Shared>, Query(query): Query<{cls}ListQuery>) -> Result<Json<{cls}Page>, StatusCode> {{
    let (page, limit) = bounds(query.page, query.limit)?;
{chr(10).join(checks)}
    let store = state.lock().unwrap();
    let matched: Vec<{cls}> = store.{key}.iter().filter(|row| {" && ".join(conditions)}).cloned().collect();
    let (items, has_more) = page_of(&matched, page, limit);
    Ok(Json({cls}Page {{ items, page, limit, total: matched.len() as u32, has_more }}))
}}
''')
        elif op == 'get':
            out.append(f'''async fn {fn}(State(state): State<Shared>, Path(id): Path<String>) -> Result<Json<{cls}>, StatusCode> {{
    state.lock().unwrap().{key}.iter().find(|row| row.id == id).cloned().map(Json).ok_or(StatusCode::NOT_FOUND)
}}
''')
        elif op == 'create':
            checks, values = [], []
            for name in r.create_required:
                item = r.field(name)
                if item.kind == 'integer':
                    checks.append(f'    nonnegative(Some(input.{snake(name)}))?;')
                elif item.enum:
                    checks.append(f'    one_of(&Some(input.{snake(name)}.clone()), {choices(name)})?;')
                else:
                    checks.append(f'    nonempty(&input.{snake(name)})?;')
            for name in r.create_optional:
                if r.field(name).enum:
                    checks.append(f'    one_of(&input.{snake(name)}, {choices(name)})?;')
            for item in r.fields:
                field = snake(item.name)
                if item.name in r.create_required:
                    values.append(f'{field}: input.{field}')
                elif item.name in r.create_optional:
                    values.append(f'{field}: input.{field}.unwrap_or_else(|| {quote(r.create_defaults[item.name])}.into())')
                elif item.name == 'createdAt':
                    values.append(f'{field}: FIXED_TIME.into()')
                elif item.kind == 'strings':
                    values.append(f'{field}: vec![]')
                else:
                    values.append(f'{field}: {rust_literal(item, r.create_defaults.get(item.name))}')
            fmt_spec = r.id_format.replace('{:', '{:').replace('d}', '}')
            out.append(f'''async fn {fn}(State(state): State<Shared>, Json(input): Json<New{cls}>) -> Result<(StatusCode, Json<{cls}>), StatusCode> {{
{chr(10).join(checks)}
    let mut store = state.lock().unwrap();
    let id = format!("{fmt_spec}", store.next_{key});
    store.next_{key} += 1;
    let row = {cls} {{ id: id.clone(), {", ".join(values)}, tenant_id: "tenant-a".into(), internal_note: format!("server-only note for {{}}", id), audit: Audit::created() }};
    store.{key}.push(row.clone());
    Ok((StatusCode::CREATED, Json(row)))
}}
''')
        elif op == 'update':
            checks, apply = [], []
            for name in r.patch:
                item = r.field(name)
                field = snake(name)
                if item.enum:
                    checks.append(f'    one_of(&input.{field}, {choices(name)})?;')
                if item.kind == 'integer':
                    checks.append(f'    nonnegative(input.{field})?;')
                target = f'Some(value)' if item.nullable else 'value'
                apply.append(f'    if let Some(value) = input.{field} {{ row.{field} = {target}; }}')
            out.append(f'''async fn {fn}(State(state): State<Shared>, Path(id): Path<String>, Json(input): Json<{cls}Patch>) -> Result<Json<{cls}>, StatusCode> {{
{chr(10).join(checks)}
    let mut store = state.lock().unwrap();
    let row = store.{key}.iter_mut().find(|row| row.id == id).ok_or(StatusCode::NOT_FOUND)?;
{chr(10).join(apply)}
    row.audit = row.audit.next();
    Ok(Json(row.clone()))
}}
''')
        elif op == 'delete':
            out.append(f'''async fn {fn}(State(state): State<Shared>, Path(id): Path<String>) -> StatusCode {{
    let mut store = state.lock().unwrap();
    let before = store.{key}.len();
    store.{key}.retain(|row| row.id != id);
    if store.{key}.len() < before {{ StatusCode::NO_CONTENT }} else {{ StatusCode::NOT_FOUND }}
}}
''')
        elif op == 'search':
            condition = ' || '.join(f'contains(&row.{snake(n)}, &input.query)' for n in r.search)
            out.append(f'''async fn {fn}(State(state): State<Shared>, Json(input): Json<SearchRequest>) -> Result<Json<{cls}Page>, StatusCode> {{
    nonempty(&input.query)?;
    let (_, limit) = bounds(Some(1), input.limit)?;
    let store = state.lock().unwrap();
    let matched: Vec<{cls}> = store.{key}.iter().filter(|row| {condition}).cloned().collect();
    let (items, has_more) = page_of(&matched, 1, limit);
    Ok(Json({cls}Page {{ items, page: 1, limit, total: matched.len() as u32, has_more }}))
}}
''')
        elif op == 'cancel':
            out.append(f'''async fn {fn}(State(state): State<Shared>, Path(id): Path<String>) -> Result<Json<{cls}>, StatusCode> {{
    let mut store = state.lock().unwrap();
    let row = store.{key}.iter_mut().find(|row| row.id == id).ok_or(StatusCode::NOT_FOUND)?;
    if row.status != "pending" && row.status != "paid" {{ return Err(StatusCode::CONFLICT); }}
    row.status = "cancelled".into();
    row.audit = row.audit.next();
    Ok(Json(row.clone()))
}}
''')
        elif op == 'tracking':
            out.append(f'''async fn {fn}(State(state): State<Shared>, Path(id): Path<String>) -> Result<Json<{cls}Tracking>, StatusCode> {{
    if !state.lock().unwrap().{key}.iter().any(|row| row.id == id) {{ return Err(StatusCode::NOT_FOUND); }}
    if !TRACKING_AVAILABLE {{ return Err(StatusCode::SERVICE_UNAVAILABLE); }}
    Ok(Json({cls}Tracking {{ shipment_id: id, events: vec![] }}))
}}
''')
    return '\n'.join(out)


# --------------------------------------------------------------------------- Python

def py_type(item, *, optional=False):
    if item.enum:
        base = 'Literal[' + ', '.join(quote(v) for v in item.enum) + ']'
    else:
        base = {'string': 'str', 'integer': 'int', 'boolean': 'bool', 'strings': 'list[str]'}[item.kind]
    return base + ' | None' if optional or item.nullable else base


def python(scale, root):
    root.mkdir(parents=True)
    lines = [f'''"""Generated Python implementation of the {scale} benchmark API with explicit a2api capabilities.

The functions are the a2api Python path; the shared BenchStore also backs the Python HTTP server.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from a2api import Application, capability
from a2api.errors import A2APIError
from pystore import BenchStore, StoreError

STORE = BenchStore({quote(scale)})
CODES = {{400: 'UPSTREAM_VALIDATION_FAILED', 404: 'RESOURCE_NOT_FOUND', 409: 'UPSTREAM_CONFLICT', 503: 'UPSTREAM_UNAVAILABLE'}}


def _call(method, *args):
    try:
        return method(*args)
    except StoreError as error:
        raise A2APIError(CODES.get(error.status, 'UPSTREAM_ERROR'), error.message, status=error.status) from None


def _public(row, fields):
    return {{name: row[name] for name in ('id', *fields)}}


class TrackingEvent(TypedDict):
    time: str
    location: str
    description: str
''']
    functions = []
    for r in resources(scale):
        public = [f.name for f in r.fields]
        lines.append(f'\nclass {r.cls}(TypedDict):\n    id: str\n' + ''.join(f'    {f.name}: {py_type(f)}\n' for f in r.fields))
        lines.append(f'\nclass {r.cls}Page(TypedDict):\n    items: list[{r.cls}]\n    page: int\n    limit: int\n    total: int\n    hasMore: bool\n')
        if 'tracking' in r.ops:
            lines.append(f'\nclass {r.cls}Tracking(TypedDict):\n    shipmentId: str\n    events: list[TrackingEvent]\n')
        lines.append(f'\n{r.key.upper()}_FIELDS = {tuple(public)!r}\n')
        for op in r.ops:
            fn = r.snake_op(op)
            functions.append(fn)
            decorator = (f'@capability(id={quote("shop." + r.key + "." + op)}, effect={quote(r.effect(op))}, '
                         f'summary={quote(r.summary(op))}, keywords={r.op_keywords(op)!r})')
            fields = r.key.upper() + '_FIELDS'
            if op == 'list':
                params = [f'{n}: {py_type(r.field(n), optional=True)} = None' for n in r.filters]
                params += ['page: int = 1', f'limit: int = {DEFAULT_LIMIT}']
                filters = '{' + ', '.join(f'{quote(n)}: {n}' for n in r.filters) + '}'
                body = (f'    result = _call(STORE.list, {quote(r.key)}, {filters}, page, limit)\n'
                        f'    return {{**result, "items": [_public(row, {fields}) for row in result["items"]]}}')
                returns = r.cls + 'Page'
            elif op == 'search':
                params = ['query: str', f'limit: int = {DEFAULT_LIMIT}']
                body = (f'    result = _call(STORE.search, {quote(r.key)}, query, limit)\n'
                        f'    return {{**result, "items": [_public(row, {fields}) for row in result["items"]]}}')
                returns = r.cls + 'Page'
            elif op == 'create':
                params = [f'{n}: {py_type(r.field(n))}' for n in r.create_required]
                params += [f'{n}: {py_type(r.field(n))} = {quote(r.create_defaults[n])}' for n in r.create_optional]
                payload = '{' + ', '.join(f'{quote(n)}: {n}' for n in (*r.create_required, *r.create_optional)) + '}'
                body = f'    return _public(_call(STORE.create, {quote(r.key)}, {payload}), {fields})'
                returns = r.cls
            elif op == 'update':
                params = ['id: str'] + [f'{n}: {py_type(r.field(n), optional=True)} = None' for n in r.patch]
                payload = '{' + ', '.join(f'{quote(n)}: {n}' for n in r.patch) + '}'
                body = f'    return _public(_call(STORE.update, {quote(r.key)}, id, {payload}), {fields})'
                returns = r.cls
            elif op == 'delete':
                params, returns = ['id: str'], 'None'
                body = f'    _call(STORE.delete, {quote(r.key)}, id)'
            elif op == 'tracking':
                params, returns = ['id: str'], r.cls + 'Tracking'
                body = f'    return _call(STORE.tracking, {quote(r.key)}, id)'
            else:  # get / cancel
                params, returns = ['id: str'], r.cls
                method = 'get' if op == 'get' else 'cancel'
                body = f'    return _public(_call(STORE.{method}, {quote(r.key)}, id), {fields})'
            lines.append(f'\n{decorator}\ndef {fn}({", ".join(params)}) -> {returns}:\n    """{r.summary(op)}"""\n{body}\n')
    lines.append('\nAPPLICATION = Application([\n' + ''.join(f'    {fn},\n' for fn in functions) + '])\n')
    (root / 'bench_service.py').write_text(''.join(lines))


def generate(out: Path):
    if out.exists():
        shutil.rmtree(out)
    for scale in SCALES:
        base = out / scale
        base.mkdir(parents=True)
        (base / 'openapi.json').write_text(json.dumps(openapi(scale), ensure_ascii=False, indent=1) + '\n')
        spring(scale, base / 'spring')
        go(scale, base / 'go')
        rust(scale, base / 'rust')
        python(scale, base / 'python')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=REPO / 'artifacts/benchmark/generated')
    args = parser.parse_args()
    print(generate(args.out))


if __name__ == '__main__':
    main()
