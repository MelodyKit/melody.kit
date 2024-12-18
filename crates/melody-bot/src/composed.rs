use melody_kit::{config::core::OwnedConfig, keyring::OwnedKeyring, setup::setup};
use miette::Diagnostic;
use thiserror::Error;

use crate::client::run;

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Setup(#[from] melody_kit::setup::Error),
    Client(#[from] crate::client::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("composed error")]
#[diagnostic(
    code(melody_discord::composed),
    help("see the report for more information")
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

    pub fn setup(error: melody_kit::setup::Error) -> Self {
        Self::new(error.into())
    }

    pub fn client(error: crate::client::Error) -> Self {
        Self::new(error.into())
    }
}

pub async fn composed<T: AsRef<str>>(
    token: T,
    config: OwnedConfig,
    keyring: OwnedKeyring,
) -> Result<(), Error> {
    let state = setup(config, keyring).await.map_err(Error::setup)?;

    run(token, state).await.map_err(Error::client)
}
