use melody_database::database::{self, Database};
use melody_redis::redis::{self, Redis};
use melody_state::state::State;
use miette::Diagnostic;
use thiserror::Error;

use crate::init::Parts;

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Redis(#[from] redis::Error),
    Database(#[from] database::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("setup failed")]
#[diagnostic(
    code(melody::app::setup),
    help("make sure the configuration is correct")
)]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn redis(error: redis::Error) -> Self {
        Self::new(error.into())
    }

    pub fn database(error: database::Error) -> Self {
        Self::new(error.into())
    }
}

pub async fn setup(parts: Parts<'_>) -> Result<State<'_>, Error> {
    let (config, keyring, hasher) = parts;

    let redis_host = config.redis.host.as_ref();
    let redis_port = config.redis.port;

    let redis = Redis::create(redis_host, redis_port)
        .await
        .map_err(Error::redis)?;

    let database = Database::create().await.map_err(Error::database)?;

    let state = State::builder()
        .database(database)
        .redis(redis)
        .config(config)
        .keyring(keyring)
        .hasher(hasher)
        .build();

    Ok(state)
}
