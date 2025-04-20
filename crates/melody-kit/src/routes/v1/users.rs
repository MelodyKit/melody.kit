use axum::{
    Json, Router,
    extract::{Path, State},
    routing::get,
};
use melody_bridge::bridge::TryBridge;
use melody_link::{id::Id, tag::StaticTag};
use melody_model::models::user::StaticUser;
use melody_state::state::{AppRouter, AppState};

use crate::errors::Error;

async fn get_user(
    State(state): State<AppState>,
    Path(user_id): Path<Id>,
) -> Result<Json<StaticUser>, Error> {
    let user = state
        .database
        .query_user(user_id)
        .await
        .map_err(Error::internal)?
        .try_bridge()
        .map_err(Error::internal)?
        .ok_or_else(|| Error::user_not_found(user_id))?;

    Ok(Json(user))
}

async fn get_user_by_tag(
    State(state): State<AppState>,
    Path(tag): Path<StaticTag>,
) -> Result<Json<StaticUser>, Error> {
    let user = state
        .database
        .query_user_by_tag(&tag)
        .await
        .map_err(Error::internal)?
        .try_bridge()
        .map_err(Error::internal)?
        .ok_or_else(|| Error::user_not_found_by_tag(&tag))?;

    Ok(Json(user))
}

pub fn router() -> AppRouter {
    Router::new()
        .route("/{user_id}", get(get_user))
        .route("/@{tag}", get(get_user_by_tag))
}
