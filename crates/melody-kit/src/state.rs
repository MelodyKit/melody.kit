use std::sync::Arc;

use axum::Router;
use bon::Builder;

use crate::{config::core::OwnedConfig, database::Database, keyring::OwnedKeyring, redis::Redis};

#[derive(Debug, Clone, Builder)]
pub struct State {
    pub database: Database,
    pub redis: Redis,
    pub config: Arc<OwnedConfig>,
    pub keyring: Arc<OwnedKeyring>,
}

pub type RouterWithState = Router<State>;
pub type RouterState = State;
