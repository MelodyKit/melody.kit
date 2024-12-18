use miette::Diagnostic;
use redis::{aio::MultiplexedConnection as Connection, Client, RedisError};
use thiserror::Error;

use crate::types::Port;

#[derive(Debug, Error, Diagnostic)]
#[error("redis failed")]
#[diagnostic(code(melody_kit::redis), help("see the report for more information"))]
pub struct Error(#[from] pub RedisError);

#[derive(Debug, Clone)]
pub struct Redis {
    pub connection: Connection,
}

impl Redis {
    pub fn new(connection: Connection) -> Self {
        Self { connection }
    }

    pub async fn create<H: AsRef<str>>(host: H, port: Port) -> Result<Self, Error> {
        let address = (host.as_ref(), port);

        let client = Client::open(address)?;

        let connection = client.get_multiplexed_tokio_connection().await?;

        Ok(Self::new(connection))
    }
}
