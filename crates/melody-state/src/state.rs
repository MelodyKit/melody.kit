use std::sync::Arc;

use axum::Router;
use bon::Builder;
use into_static::IntoStatic;
use melody_config::config::core::Config;
use melody_database::database::Database;
use melody_hash::hash::Hasher;
use melody_keyring::keyring::Keyring;
use melody_redis::redis::Redis;

#[derive(Debug, Clone, Builder)]
pub struct State<'s> {
    pub database: Database,
    pub redis: Redis,
    pub config: Config<'s>,
    pub keyring: Keyring<'s>,
    pub hasher: Hasher,
}

impl IntoStatic for State<'_> {
    type Static = State<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .database(self.database)
            .redis(self.redis)
            .hasher(self.hasher)
            .config(self.config.into_static())
            .keyring(self.keyring.into_static())
            .build()
    }
}

pub type StaticState = State<'static>;

pub type NoState = ();

pub type AppState = Arc<StaticState>;

pub type AppRouter = Router<AppState>;
pub type StatelessRouter = Router<NoState>;
