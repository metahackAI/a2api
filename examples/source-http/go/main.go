package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "strings"
    "sync"
)

type Item struct {
    ID string `json:"id"`
    Name string `json:"name"`
    InternalNote string `json:"internalNote"`
}
type ItemView struct { ID string `json:"id"`; Name string `json:"name"` }
type NewItem struct { Name string `json:"name"` }
type PatchItem struct { Name *string `json:"name"` }
type Filter struct { Q string `json:"q"` }

var mu sync.Mutex
var sequence = 100
var items = map[string]Item{"I-1": {ID:"I-1", Name:"original", InternalNote:"server-only"}}

func getItem(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    id := r.PathValue("id")
    var out Item
    out, ok := items[id]
    if !ok { http.NotFound(w,r); return }
    w.Header().Set("Content-Type","application/json")
    json.NewEncoder(w).Encode(out)
}
func headItem(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    id := r.PathValue("id")
    if _, ok := items[id]; !ok { http.NotFound(w,r); return }
    w.WriteHeader(http.StatusOK)
}
func createItem(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    var input NewItem
    if json.NewDecoder(r.Body).Decode(&input) != nil || input.Name == "" { http.Error(w,"invalid",400); return }
    sequence++
    out := Item{ID:fmt.Sprintf("I-%d",sequence), Name:input.Name, InternalNote:"server-only"}
    items[out.ID] = out
    w.Header().Set("Content-Type","application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(out)
}
func replaceItem(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    id := r.PathValue("id")
    if _, ok := items[id]; !ok { http.NotFound(w,r); return }
    var input NewItem
    if json.NewDecoder(r.Body).Decode(&input) != nil || input.Name == "" { http.Error(w,"invalid",400); return }
    out := Item{ID:id, Name:input.Name, InternalNote:"server-only"}
    items[id] = out
    w.Header().Set("Content-Type","application/json")
    json.NewEncoder(w).Encode(out)
}
func patchItem(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    id := r.PathValue("id")
    var out Item
    out, ok := items[id]
    if !ok { http.NotFound(w,r); return }
    var input PatchItem
    if json.NewDecoder(r.Body).Decode(&input) != nil { http.Error(w,"invalid",400); return }
    if input.Name != nil { out.Name = *input.Name }
    items[id] = out
    w.Header().Set("Content-Type","application/json")
    json.NewEncoder(w).Encode(out)
}
func deleteItem(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    id := r.PathValue("id")
    if _, ok := items[id]; !ok { http.NotFound(w,r); return }
    delete(items,id)
    w.WriteHeader(http.StatusNoContent)
}
func searchItems(w http.ResponseWriter, r *http.Request) {
    mu.Lock(); defer mu.Unlock()
    var input Filter
    if json.NewDecoder(r.Body).Decode(&input) != nil { http.Error(w,"invalid",400); return }
    result := []ItemView{}
    for _, item := range items {
        if strings.Contains(item.Name,input.Q) { result = append(result,ItemView{ID:item.ID,Name:item.Name}) }
    }
    w.Header().Set("Content-Type","application/json")
    json.NewEncoder(w).Encode(result)
}
func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /items/{id}", getItem)
    mux.HandleFunc("HEAD /items/{id}", headItem)
    mux.HandleFunc("POST /items", createItem)
    mux.HandleFunc("PUT /items/{id}", replaceItem)
    mux.HandleFunc("PATCH /items/{id}", patchItem)
    mux.HandleFunc("DELETE /items/{id}", deleteItem)
    mux.HandleFunc("POST /items/search", searchItems)
    if err := http.ListenAndServe("127.0.0.1:"+os.Args[1],mux); err != nil { panic(err) }
}
