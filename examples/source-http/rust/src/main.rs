use axum::{extract::{Path, Json, State}, http::StatusCode, routing::{get, post}, Router};
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, sync::{Arc, Mutex}};

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct Item { id: String, name: String, internal_note: String }
#[derive(Serialize)]
struct ItemView { id: String, name: String }
#[derive(Deserialize)]
struct NewItem { name: String }
#[derive(Deserialize)]
struct PatchItem { name: Option<String> }
#[derive(Deserialize)]
struct Filter { q: Option<String> }
struct Store { items: HashMap<String, Item>, sequence: u32 }
type Shared = Arc<Mutex<Store>>;

async fn get_item(State(state): State<Shared>, Path(id): Path<String>) -> Result<Json<Item>, StatusCode> {
    state.lock().unwrap().items.get(&id).cloned().map(Json).ok_or(StatusCode::NOT_FOUND)
}
async fn head_item(State(state): State<Shared>, Path(id): Path<String>) -> StatusCode {
    if state.lock().unwrap().items.contains_key(&id) { StatusCode::OK } else { StatusCode::NOT_FOUND }
}
async fn create_item(State(state): State<Shared>, Json(input): Json<NewItem>) -> (StatusCode, Json<Item>) {
    let mut store = state.lock().unwrap(); store.sequence += 1;
    let item = Item { id: format!("I-{}", store.sequence), name: input.name, internal_note: "server-only".into() };
    store.items.insert(item.id.clone(), item.clone());
    (StatusCode::CREATED, Json(item))
}
async fn replace_item(State(state): State<Shared>, Path(id): Path<String>, Json(input): Json<NewItem>) -> Result<Json<Item>, StatusCode> {
    let mut store = state.lock().unwrap();
    if !store.items.contains_key(&id) { return Err(StatusCode::NOT_FOUND); }
    let item = Item { id: id.clone(), name: input.name, internal_note: "server-only".into() };
    store.items.insert(id, item.clone()); Ok(Json(item))
}
async fn patch_item(State(state): State<Shared>, Path(id): Path<String>, Json(input): Json<PatchItem>) -> Result<Json<Item>, StatusCode> {
    let mut store = state.lock().unwrap();
    let item = store.items.get_mut(&id).ok_or(StatusCode::NOT_FOUND)?;
    if let Some(name) = input.name { item.name = name; } Ok(Json(item.clone()))
}
async fn delete_item(State(state): State<Shared>, Path(id): Path<String>) -> StatusCode {
    if state.lock().unwrap().items.remove(&id).is_some() { StatusCode::NO_CONTENT } else { StatusCode::NOT_FOUND }
}
async fn search_items(State(state): State<Shared>, Json(input): Json<Filter>) -> Json<Vec<ItemView>> {
    let query = input.q.unwrap_or_default();
    Json(state.lock().unwrap().items.values().filter(|item| item.name.contains(&query))
        .map(|item| ItemView { id:item.id.clone(), name:item.name.clone() }).collect())
}

#[tokio::main]
async fn main() {
    let state = Arc::new(Mutex::new(Store { sequence:100, items: HashMap::from([
        ("I-1".into(), Item { id:"I-1".into(), name:"original".into(), internal_note:"server-only".into() })]) }));
    let app = Router::new()
        .route("/items/{id}", get(get_item).head(head_item).put(replace_item).patch(patch_item).delete(delete_item))
        .route("/items", post(create_item))
        .route("/items/search", post(search_items))
        .with_state(state);
    let port = std::env::args().nth(1).expect("port");
    let listener = tokio::net::TcpListener::bind(format!("127.0.0.1:{port}")).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
