use miette::Diagnostic;
use redis::{Client, RedisError, aio::MultiplexedConnection as Connection};
use thiserror::Error;

pub type Port = u16;

#[derive(Debug, Error, Diagnostic)]
#[error("redis failed")]
#[diagnostic(code(melody::redis), help("see the report for more information"))]
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
