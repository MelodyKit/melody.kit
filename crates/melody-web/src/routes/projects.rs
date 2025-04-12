use axum::{Router, extract::Path, response::Redirect, routing::get};
use melody_state::state::AppRouter;

pub const PROJECTS: &str = "https://github.com/MelodyKit";

async fn redirect_projects(Path(name): Path<String>) -> Redirect {
    let url = format!("{PROJECTS}/{name}");

    Redirect::to(url.as_str())
}

pub fn router() -> AppRouter {
    Router::new().route("/{name}", get(redirect_projects))
}
