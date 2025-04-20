use std::fmt::Display;

use axum::{
    Router,
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Redirect, Response},
    routing::get,
};
use maud::Markup;
use melody_bridge::bridge::Bridge;
use melody_state::state::{AppRouter, AppState};

use crate::templates::{index::index, not_found::not_found};

async fn get_index(State(state): State<AppState>) -> Markup {
    let optional_statistics = state
        .database
        .query_statistics()
        .await
        .ok() // ignore query errors
        .map(Bridge::bridge);

    index(optional_statistics.as_ref())
}

async fn fallback() -> Response {
    (StatusCode::NOT_FOUND, not_found()).into_response()
}

pub fn redirect_domain<S: Display, D: Display>(name: S, domain: D) -> Redirect {
    let string = format!("https://{name}.{domain}/");

    Redirect::to(string.as_str())
}

async fn redirect_open(State(state): State<AppState>) -> Redirect {
    redirect_domain(
        state.config.context.open.get(),
        state.config.context.domain.get(),
    )
}

async fn redirect_docs(State(state): State<AppState>) -> Redirect {
    redirect_domain(
        state.config.context.docs.get(),
        state.config.context.domain.get(),
    )
}

async fn redirect_dev(State(state): State<AppState>) -> Redirect {
    redirect_domain(
        state.config.context.dev.get(),
        state.config.context.domain.get(),
    )
}

async fn redirect_api(State(state): State<AppState>) -> Redirect {
    redirect_domain(
        state.config.context.api.get(),
        state.config.context.domain.get(),
    )
}

pub fn router() -> AppRouter {
    Router::new()
        .fallback(fallback)
        .route("/", get(get_index))
        // domain redirects
        .route("/open", get(redirect_open))
        .route("/docs", get(redirect_docs))
        .route("/dev", get(redirect_dev))
        .route("/api", get(redirect_api))
}
