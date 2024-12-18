use miette::Diagnostic;
use thiserror::Error;

use crate::{
    config::core::OwnedConfig, keyring::OwnedKeyring, run::run, setup::setup, types::Port,
};

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Setup(#[from] crate::setup::Error),
    Run(#[from] crate::run::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("composed error")]
#[diagnostic(
    code(melody_kit::composed),
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

    pub fn setup(error: crate::setup::Error) -> Self {
        Self::new(error.into())
    }

    pub fn run(error: crate::run::Error) -> Self {
        Self::new(error.into())
    }
}

pub async fn composed<H: AsRef<str>>(
    host: H,
    port: Port,
    config: OwnedConfig,
    keyring: OwnedKeyring,
) -> Result<(), Error> {
    let state = setup(config, keyring).await.map_err(Error::setup)?;

    run(host, port, state).await.map_err(Error::run)
}
