use axum::Router;
use melody_state::state::AppRouter;

pub mod artists;
pub mod statistics;
pub mod users;

pub fn router() -> AppRouter {
    Router::new()
        .nest("/artists", artists::router())
        .nest("/statistics", statistics::router())
        .nest("/users", users::router())
}
