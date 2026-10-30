"""Static source extraction: supported facts, unsupported diagnostics, no execution."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from a2api import A2APIError, HTTPDeployment, convert
from a2api.importers import SpringSourceImporter, GoSourceImporter, RustSourceImporter
from a2api.ir import thaw

HAS_SOURCE = all(importlib.util.find_spec(name) for name in ('tree_sitter', 'tree_sitter_java', 'tree_sitter_go', 'tree_sitter_rust'))
ROOT = Path(__file__).resolve().parents[1]
CASES = [(SpringSourceImporter, 'spring/src/main/java', 'java'), (GoSourceImporter, 'go', 'go'), (RustSourceImporter, 'rust/src', 'rs')]


@unittest.skipUnless(HAS_SOURCE, 'Install a2api[source]')
class SourceImporterTests(unittest.TestCase):
    def source(self, cls, code, extension):
        folder = tempfile.TemporaryDirectory();self.addCleanup(folder.cleanup)
        Path(folder.name, 'sample.' + extension).write_text(code)
        return cls.from_directory(folder.name, namespace='sample')

    def test_three_actual_example_sources_extract_seven_routes_without_openapi(self):
        for cls, directory, _ in CASES:
            with self.subTest(language=cls.__name__):
                source = cls.from_directory(ROOT / 'examples/source-http' / directory, namespace='sample')
                records = list(source.iter_operations())
                self.assertEqual(len(records), 7)
                self.assertTrue(all(r.status == 'imported' for r in records), [r.summary() for r in records])
                self.assertEqual({r.method for r in records}, {'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'})
                self.assertFalse(hasattr(source, 'document'))
                for record in records:
                    self.assertIn(':', record.location)
                    self.assertIn('result', record.operation.output_schema['properties'])
                    record.http_route('http://127.0.0.1:1')
                selected = next(r for r in records if r.method == 'GET')
                app = convert(source, operations={selected.operation_id: {'effect': 'read', 'select': ['id', 'name']}},
                              deployment=HTTPDeployment('http://127.0.0.1:1'))
                descriptor = app.describe(selected.id)
                self.assertEqual(set(descriptor), {'id', 'version', 'summary', 'effects', 'inputSchema', 'outputSchema'})
                self.assertNotIn('internalNote', json.dumps(descriptor))
                self.assertNotIn('location', descriptor)
                self.assertEqual({d['id'] for d in app.descriptors()}, {selected.id})

    def test_spring_generic_inheritance_jackson_validation_query_default_and_principal(self):
        source = self.source(SpringSourceImporter, '''
            class Base { public String id; }
            class Envelope<T> { public T payload; }
            class Input extends Base { @NotBlank @JsonProperty("displayName") public String name;
                @JsonIgnore public String password; @NotEmpty @Size(max=3) public List<String> tags; }
            @RestController @RequestMapping("/v1") class Api {
              // @DeleteMapping("/fake") is a comment, not an endpoint.
              @PostMapping("/query") @ResponseStatus(HttpStatus.CREATED)
              public ResponseEntity<Envelope<Input>> search(@RequestBody @Valid Input input,
                 @RequestParam(defaultValue="2") int page, @AuthenticationPrincipal UserDetail who) {
                 return ResponseEntity.ok(null);
              }
            }''', 'java')
        result = next(source.iter_operations())
        self.assertEqual(result.status, 'imported', result.summary())
        inputs = thaw(result.operation.input_schema)
        self.assertEqual(inputs['properties']['body']['required'], ['displayName', 'tags'])
        self.assertEqual(inputs['properties']['body']['properties']['tags']['maxItems'], 3)
        self.assertEqual(inputs['properties']['body']['properties']['tags']['minItems'], 1)
        self.assertEqual(inputs['properties']['query']['properties']['page']['default'], 2)
        self.assertNotIn('query', inputs['required'])
        self.assertNotIn('who', json.dumps(inputs))
        self.assertNotIn('password', json.dumps(inputs))
        self.assertIn('id', inputs['properties']['body']['properties'])
        self.assertIn('payload', result.operation.output_schema['properties']['result']['properties'])
        self.assertEqual(result.operation.output_schema['properties']['httpStatus']['enum'], (200,))
        self.assertEqual(result.path, '/v1/query')

    def test_dynamic_route_unknown_dto_and_custom_serialization_are_diagnostic(self):
        cases = [
            (SpringSourceImporter, 'java', '@RestController class Api { @GetMapping(Paths.URL) public String get(){return "x";} }'),
            (SpringSourceImporter, 'java', '@RestController class Api { @GetMapping("/x") public Foreign get(){return null;} }'),
            (SpringSourceImporter, 'java', 'record Input(String q){} @RestController class Api { @GetMapping("/x") public int get(@RequestBody Input body){return 1;} }'),
            (SpringSourceImporter, 'java', 'class Item { @JsonSerialize(using=Codec.class) public String value; } @RestController class Api { @GetMapping("/x") public Item get(){return null;} }'),
            (SpringSourceImporter, 'java', 'class Item { @JsonProperty(access=JsonProperty.Access.WRITE_ONLY) public String secret; } @RestController class Api { @GetMapping("/x") public Item get(){return null;} }'),
            (SpringSourceImporter, 'java', '@JsonIgnoreProperties({"secret"}) class Item { public String secret; } @RestController class Api { @GetMapping("/x") public Item get(){return null;} }'),
            (GoSourceImporter, 'go', 'package main\nfunc main(){http.HandleFunc(route, handler)}'),
            (GoSourceImporter, 'go', 'package main\nfunc main(){http.HandleFunc("UPDATE /x", handler)}'),
            (RustSourceImporter, 'rs', 'fn main(){Router::new().route(dynamic_path, get(handler));}'),
            (RustSourceImporter, 'rs', 'async fn get_item()->Json<Foreign>{todo!()} fn main(){Router::new().route("/x",get(get_item));}'),
        ]
        for cls, extension, code in cases:
            with self.subTest(language=cls.__name__, code=code[:50]):
                source = self.source(cls, code, extension)
                records = list(source.iter_operations())
                self.assertTrue(records)
                self.assertTrue(all(r.status == 'unsupported' for r in records), [r.summary() for r in records])
                self.assertTrue(all(r.diagnostics for r in records))
                with self.assertRaises(A2APIError) as caught:
                    convert(source, operations={records[0].operation_id: {'effect': 'read'}}, deployment=HTTPDeployment('http://127.0.0.1:1'))
                self.assertEqual(caught.exception.code, 'CONVERT_OPERATION_UNSUPPORTED')

    def test_go_json_tags_pointers_slices_and_omitted_private_fields(self):
        source = self.source(GoSourceImporter, '''package main
          type Item struct { Label *string `json:"name,omitempty"`; Values []int `json:"values"`; Hidden string `json:"-"`; private string }
          func get(w http.ResponseWriter,r *http.Request){json.NewEncoder(w).Encode(Item{})}
          func main(){http.HandleFunc("GET /x",get)}''', 'go')
        result = next(source.iter_operations())
        self.assertEqual(result.status, 'imported', result.summary())
        schema = thaw(result.operation.output_schema)['properties']['result']
        self.assertEqual(set(schema['properties']), {'name', 'values'})
        self.assertIn({'type': 'null'}, schema['properties']['name']['anyOf'])
        self.assertEqual(schema['properties']['values']['anyOf'][0]['items']['type'], 'integer')
        self.assertIn('values', schema['required'])

    def test_rust_serde_names_option_default_and_query_path(self):
        source = self.source(RustSourceImporter, '''
          #[serde(rename_all="camelCase")] struct Item { item_name:String, #[serde(skip)] secret:String }
          struct Search { #[serde(default)] q:Option<String> }
          async fn find(Path(id):Path<String>, Query(query):Query<Search>)->Json<Item>{todo!()}
          fn main(){Router::new().route("/x/{id}",get(find));}''', 'rs')
        result = next(source.iter_operations())
        self.assertEqual(result.status, 'imported', result.summary())
        self.assertEqual(set(result.operation.output_schema['properties']['result']['properties']), {'itemName'})
        self.assertEqual(result.operation.input_schema['required'], ('path',))
        self.assertEqual(result.operation.input_schema['properties']['query']['required'], ())

    def test_rust_custom_serde_is_not_silently_treated_as_plain_struct(self):
        source = self.source(RustSourceImporter, '''
          struct Item { #[serde(with="codec")] value:String }
          async fn get_item()->Json<Item>{todo!()}
          fn main(){Router::new().route("/x",get(get_item));}''', 'rs')
        record = next(source.iter_operations())
        self.assertEqual(record.status, 'unsupported')
        self.assertIn('Serde', record.diagnostics[0]['detail'])

    def test_syntax_errors_and_ambiguous_handlers_are_not_guessed(self):
        source = self.source(GoSourceImporter, 'package main\nfunc main( {', 'go')
        self.assertEqual(list(source.iter_operations()), [])
        self.assertEqual(source.diagnostics[0]['code'], 'SOURCE_PARSE_ERROR')
        with self.assertRaises(A2APIError):list(source.iter_operations({'missing'}))
        with self.assertRaises(A2APIError) as caught:
            self.source(SpringSourceImporter, '@RestController class Api { @GetMapping("/x") public int get(){return 1;} @GetMapping("/y") public int get(int id){return 2;} }', 'java')
        self.assertEqual(caught.exception.code, 'DUPLICATE_SOURCE_OPERATION')

    def test_context_changing_or_indirect_routes_are_not_advertised_as_complete(self):
        for cls, extension, code in [
            (SpringSourceImporter, 'java', '@ControllerAdvice class Advice {} @RestController class Api { @GetMapping("/x") public int get(){return 1;} }'),
            (SpringSourceImporter, 'java', '@RestController class Api { @GetMapping(value="/x",params="version=2") public int get(){return 1;} }'),
            (GoSourceImporter, 'go', 'package main\ntype Item struct{ Name string }\nfunc get(w http.ResponseWriter,r *http.Request){var body Item; decoder:=json.NewDecoder(r.Body);decoder.Decode(&body);json.NewEncoder(w).Encode(body)}\nfunc main(){http.HandleFunc("POST /x",get)}'),
            (RustSourceImporter, 'rs', 'struct Item{id:String} async fn get_item()->Json<Item>{todo!()} fn main(){Router::new().nest("/prefix",Router::new().route("/x",get(get_item)));}')]:
            with self.subTest(language=cls.__name__):
                source = self.source(cls, code, extension)
                self.assertTrue(list(source.iter_operations()))
                self.assertTrue(all(r.status == 'unsupported' for r in source.iter_operations()))

    def test_go_custom_json_method_and_binary_codec_require_explicit_schema(self):
        for code in [
            'package main\ntype Item struct { Name string }\nfunc (i Item) MarshalJSON()([]byte,error){return nil,nil}\nfunc get(w http.ResponseWriter,r *http.Request){json.NewEncoder(w).Encode(Item{})}\nfunc main(){http.HandleFunc("GET /x",get)}',
            'package main\ntype Item struct { Binary []byte }\nfunc get(w http.ResponseWriter,r *http.Request){json.NewEncoder(w).Encode(Item{})}\nfunc main(){http.HandleFunc("GET /x",get)}']:
            record = next(self.source(GoSourceImporter, code, 'go').iter_operations())
            self.assertEqual(record.status, 'unsupported')

    def test_java_nested_validation_only_cascades_with_valid(self):
        source = self.source(SpringSourceImporter, '''
          class Child { @NotBlank public String name; }
          class Input { public Child plain; @Valid public Child checked; }
          @RestController class Api { @PostMapping("/x") public int post(@Valid @RequestBody Input input){return 1;} }
        ''', 'java')
        row = next(source.iter_operations())
        props = row.operation.input_schema['properties']['body']['properties']
        self.assertEqual(props['plain']['anyOf'][0]['required'], ())
        self.assertEqual(props['checked']['anyOf'][0]['required'], ('name',))

    def test_source_loading_does_not_follow_symlinks_or_execute_build_files(self):
        with tempfile.TemporaryDirectory() as folder, tempfile.TemporaryDirectory() as outside:
            root = Path(folder)
            Path(outside, 'Evil.java').write_text('@RestController class Evil { @GetMapping("/evil") public int get(){return 1;} }')
            root.joinpath('link.java').symlink_to(Path(outside, 'Evil.java'))
            root.joinpath('pom.xml').write_text('INVALID XML MUST NOT EXECUTE')
            source = SpringSourceImporter.from_directory(root)
            self.assertEqual(list(source.iter_operations()), [])


if __name__ == '__main__':unittest.main()
