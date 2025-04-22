use axum::Router;

use melody_state::state::AppRouter;

use crate::errors::Error;

pub mod v1;

async fn fallback() -> Error {
    Error::fallback()
}

pub fn router() -> AppRouter {
    Router::new().fallback(fallback).nest("/v1", v1::router())
}
