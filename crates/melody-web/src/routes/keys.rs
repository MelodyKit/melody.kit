use axum::{
    Router,
    extract::Path,
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::get,
};
use melody_state::state::AppRouter;
use tokio::fs::read_to_string;

pub const KEYS: &str = "keys";

async fn get_key(Path(name): Path<String>) -> Response {
    let key_path = format!("{KEYS}/{name}.key");

    read_to_string(key_path)
        .await
        .map_or_else(
            |_| (StatusCode::NOT_FOUND, format!("can not find `{name}` key")),
            |key| (StatusCode::OK, key),
        )
        .into_response()
}

pub fn router() -> AppRouter {
    Router::new().route("/{name}", get(get_key))
}
