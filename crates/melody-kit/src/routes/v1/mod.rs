use axum::Router;
use melody_state::state::AppRouter;

pub mod statistics;
pub mod users;

pub fn router() -> AppRouter {
    Router::new()
        .nest("/statistics", statistics::router())
        .nest("/users", users::router())
}
