use axum::{
    extract::{Path, State},
    routing::get,
    Json, Router,
};
use uuid::Uuid;

use crate::{
    errors::Error,
    models::user::OwnedUser,
    state::{RouterState, RouterWithState},
};

async fn get_user(
    State(state): State<RouterState>,
    Path(user_id): Path<Uuid>,
) -> Result<Json<OwnedUser>, Error> {
    let user = state
        .database
        .query_user(user_id)
        .await
        .map_err(|_| Error::internal())?;

    user.map(Json).ok_or_else(|| Error::user_not_found(user_id))
}

async fn get_user_by_tag(
    State(state): State<RouterState>,
    Path(tag): Path<String>,
) -> Result<Json<OwnedUser>, Error> {
    let tag: &str = tag.as_ref();

    let user = state
        .database
        .query_user_by_tag(tag)
        .await
        .map_err(|_| Error::internal())?;

    user.map(Json)
        .ok_or_else(|| Error::user_not_found_by_tag(tag))
}

pub fn router() -> RouterWithState {
    Router::new()
        .route("/:user_id", get(get_user))
        .route("/@:tag", get(get_user_by_tag))
}
