use std::path::Path;

use from_path::FromPath;
use melody_config::{
    config::{core::Config, path},
    load,
};
use melody_hash::hash::{Hasher, HasherError};
use melody_keyring::keyring::{self, Keyring};
use miette::Diagnostic;
use thiserror::Error;

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    ExpandTilde(#[from] expand_tilde::Error),
    Config(#[from] load::Error),
    Keyring(#[from] keyring::Error),
    Hasher(#[from] HasherError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("initialization error")]
#[diagnostic(code(melody::app::init), help("see the report for more information"))]
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

    pub fn config(error: load::Error) -> Self {
        Self::new(error.into())
    }

    pub fn keyring(error: keyring::Error) -> Self {
        Self::new(error.into())
    }

    pub fn hasher(error: HasherError) -> Self {
        Self::new(error.into())
    }
}

pub type Parts<'p> = (Config<'p>, Keyring<'p>, Hasher);

pub type StaticParts = Parts<'static>;

pub fn init<P: AsRef<Path>>(option: Option<P>) -> Result<StaticParts, Error> {
    let path = path::or_default(option).map_err(Error::expand_tilde)?;

    let config = Config::from_path(path).map_err(Error::config)?;

    let keyring = Keyring::load_with(&config.keyring).map_err(Error::keyring)?;

    let hasher = Hasher::create(&config.hash).map_err(Error::hasher)?;

    Ok((config, keyring, hasher))
}
