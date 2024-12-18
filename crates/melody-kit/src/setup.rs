use std::sync::Arc;

use miette::Diagnostic;
use thiserror::Error;

use crate::{
    config::core::OwnedConfig, database::Database, keyring::OwnedKeyring, redis::Redis,
    state::State,
};

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Redis(#[from] crate::redis::Error),
    Database(#[from] crate::database::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("setup failed")]
#[diagnostic(code(melody_kit::router), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn redis(error: crate::redis::Error) -> Self {
        Self::new(error.into())
    }

    pub fn database(error: crate::database::Error) -> Self {
        Self::new(error.into())
    }
}

pub async fn setup(config: OwnedConfig, keyring: OwnedKeyring) -> Result<State, Error> {
    let redis_host = config.redis.host.as_ref();
    let redis_port = config.redis.port;

    let redis = Redis::create(redis_host, redis_port)
        .await
        .map_err(Error::redis)?;

    let database = Database::create().await.map_err(Error::database)?;

    let state = State::builder()
        .database(database)
        .redis(redis)
        .config(Arc::new(config))
        .keyring(Arc::new(keyring))
        .build();

    Ok(state)
}
