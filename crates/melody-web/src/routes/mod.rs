pub mod email;
pub mod keys;
pub mod projects;

use axum::{Router, extract::State, response::Redirect, routing::get};
use maud::Markup;
use melody_bridge::bridge::Bridge;
use melody_state::state::{AppRouter, AppState};

use crate::templates::index::index;

async fn get_index(State(state): State<AppState>) -> Markup {
    let optional_statistics = state
        .database
        .query_statistics()
        .await
        .ok() // ignore database errors
        .bridge()
        .ok() // ignore bridge errors
        .flatten();

    index(optional_statistics)
}

pub const OPEN: &str = "https://open.melodykit.app/";

pub const DOCS: &str = "https://docs.melodykit.app/";
pub const DEV: &str = "https://dev.melodykit.app/";

async fn redirect_open() -> Redirect {
    Redirect::to(OPEN)
}

async fn redirect_docs() -> Redirect {
    Redirect::to(DOCS)
}

async fn redirect_dev() -> Redirect {
    Redirect::to(DEV)
}

pub const DISCORD: &str = "https://discord.com/invite/NeKqH6ng2G";

pub const GITHUB: &str = "https://github.com/MelodyKit";

pub const X: &str = "https://x.com/MelodyKitApp";

pub const REDDIT: &str = "https://reddit.com/r/MelodyKit";
pub const YOUTUBE: &str = "https://youtube.com/MelodyKit";

pub const TELEGRAM: &str = "https://t.me/MelodyKitApp";

async fn redirect_discord() -> Redirect {
    Redirect::to(DISCORD)
}

async fn redirect_github() -> Redirect {
    Redirect::to(GITHUB)
}

async fn redirect_x() -> Redirect {
    Redirect::to(X)
}

async fn redirect_reddit() -> Redirect {
    Redirect::to(REDDIT)
}

async fn redirect_youtube() -> Redirect {
    Redirect::to(YOUTUBE)
}

async fn redirect_telegram() -> Redirect {
    Redirect::to(TELEGRAM)
}

pub fn router() -> AppRouter {
    Router::new()
        .route("/", get(get_index))
        // domain redirects
        .route("/open", get(redirect_open))
        .route("/docs", get(redirect_docs))
        .route("/dev", get(redirect_dev))
        // other redirects
        .route("/discord", get(redirect_discord))
        .route("/github", get(redirect_github))
        .route("/x", get(redirect_x))
        .route("/reddit", get(redirect_reddit))
        .route("/youtube", get(redirect_youtube))
        .route("/telegram", get(redirect_telegram))
        // nested routes
        .nest("/keys", keys::router())
        .nest("/email", email::router())
        .nest("/projects", projects::router())
}
