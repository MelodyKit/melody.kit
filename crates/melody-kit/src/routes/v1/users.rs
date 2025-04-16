use axum::{
    Json, Router,
    extract::{Path, State},
    routing::get,
};
use melody_bridge::bridge::Bridge;
use melody_link::id::Id;
use melody_model::models::user::User;
use melody_state::state::{AppRouter, AppState};

use crate::errors::Error;

async fn get_user(
    State(state): State<AppState>,
    Path(user_id): Path<Id>,
) -> Result<Json<UserResponse>, Error> {
    let optional_user = state
        .database
        .query_user(user_id)
        .await
        .map_err(Error::internal)?
        .bridge()
        .map_err(Error::internal)?;

    user.map(Json).ok_or_else(|| Error::user_not_found(user_id))
}

async fn get_user_by_tag(
    State(state): State<AppState>,
    Path(tag): Path<String>,
) -> Result<Json<UserResponse>, Error> {
    let user = state
        .database
        .query_user_by_tag(tag.as_ref())
        .await
        .map_err(Error::internal)?
        .bridge()
        .map_err(Error::internal)?;

    user.map(Json)
        .ok_or_else(|| Error::user_not_found_by_tag(tag))
}

pub fn router() -> AppRouter {
    Router::new()
        .route("/{user_id}", get(get_user))
        .route("/@{tag}", get(get_user_by_tag))
}
