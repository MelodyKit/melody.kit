use std::path::Path;

use expand_tilde::ExpandTilde;
use miette::Diagnostic;
use thiserror::Error;

use crate::{
    config::{
        core::{Config, OwnedConfig},
        default::DEFAULT_PATH,
    },
    keyring::{Keyring, OwnedKeyring},
    load::Load,
};

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    ExpandTilde(#[from] expand_tilde::Error),
    Config(#[from] crate::config::core::Error),
    Keyring(#[from] crate::keyring::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("initialization error")]
#[diagnostic(code(melody_kit::init), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn expand_tilde(error: expand_tilde::Error) -> Self {
        Self::new(error.into())
    }

    pub fn config(error: crate::config::core::Error) -> Self {
        Self::new(error.into())
    }

    pub fn keyring(error: crate::keyring::Error) -> Self {
        Self::new(error.into())
    }
}

pub fn init<P: AsRef<Path>>(path: Option<P>) -> Result<(OwnedConfig, OwnedKeyring), Error> {
    let path = path
        .map_or_else(|| DEFAULT_PATH.expand_tilde(), |path| path.expand_tilde())
        .map_err(Error::expand_tilde)?;

    let config = Config::load(path).map_err(Error::config)?;

    let keyring = Keyring::load_with(&config.keyring).map_err(Error::keyring)?;

    Ok((config, keyring))
}
