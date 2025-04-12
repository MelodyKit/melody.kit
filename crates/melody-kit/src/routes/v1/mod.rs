use axum::{Json, Router, extract::State, routing::get};
use melody_bridge::bridge::Bridge;
use melody_model::models::statistics::Statistics;
use melody_state::state::{AppRouter, AppState};

use crate::errors::Error;

async fn get_statistics(State(state): State<AppState>) -> Result<Json<Statistics>, Error> {
    let statistics = state
        .database
        .query_statistics()
        .await
        .map_err(Error::internal)?
        .bridge()
        .map_err(Error::internal)?;

    Ok(Json(statistics))
}

pub fn router() -> AppRouter {
    Router::new().route("/statistics", get(get_statistics))
}
