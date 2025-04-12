use axum::{Router, extract::Path, response::Redirect, routing::get};
use melody_state::state::AppRouter;

async fn redirect_email(Path(name): Path<String>) -> Redirect {
    let uri = format!("mailto:{name}@melodykit.app");

    Redirect::to(uri.as_str())
}

pub fn router() -> AppRouter {
    Router::new().route("/{name}", get(redirect_email))
}
