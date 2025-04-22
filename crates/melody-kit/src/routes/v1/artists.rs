use axum::{
    Json, Router,
    extract::{Path, State},
    routing::get,
};
use melody_bridge::bridge::TryBridge;
use melody_link::id::Id;
use melody_model::models::artist::StaticArtist;
use melody_state::state::{AppRouter, AppState};

use crate::errors::Error;

async fn get_artist(
    State(state): State<AppState>,
    Path(artist_id): Path<Id>,
) -> Result<Json<StaticArtist>, Error> {
    let artist = state
        .database
        .query_artist(artist_id)
        .await
        .map_err(Error::internal)?
        .try_bridge()
        .map_err(Error::internal)?
        .ok_or_else(|| Error::artist_not_found(artist_id))?;

    Ok(Json(artist))
}

pub fn router() -> AppRouter {
    Router::new().route("/{artist_id}", get(get_artist))
}
