use axum::Router;

use crate::state::RouterWithState;

pub mod v1;

pub fn router() -> RouterWithState {
    Router::new().nest("/v1", v1::router())
}
