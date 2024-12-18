use axum::{extract::State, routing::get, Json, Router};

use crate::{
    errors::Error,
    models::statistics::Statistics,
    state::{RouterState, RouterWithState},
};

pub mod users;

async fn get_statistics(State(state): State<RouterState>) -> Result<Json<Statistics>, Error> {
    let statistics = state
        .database
        .query_statistics()
        .await
        .map_err(|_| Error::internal())?;

    Ok(Json(statistics))
}

pub fn router() -> RouterWithState {
    Router::new()
        .route("/statistics", get(get_statistics))
        .nest("/users", users::router())
}
