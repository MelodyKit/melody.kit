use axum::{Json, Router, extract::State, routing::get};
use melody_model::models::statistics::Statistics;
use melody_state::state::{AppRouter, AppState};

use crate::errors::Error;

async fn get_statistics(State(state): State<AppState>) -> Result<Json<Statistics>, Error> {
    let schema = state
        .database
        .query_statistics()
        .await
        .map_err(Error::internal)?;

    let statistics = Statistics::from_schema(schema);

    Ok(Json(statistics))
}

// pub mod users;

pub fn router() -> AppRouter {
    Router::new().route("/statistics", get(get_statistics)) // .nest("/users", users::router())
}
