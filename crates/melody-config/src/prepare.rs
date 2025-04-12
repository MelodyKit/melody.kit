use std::fs::{create_dir_all, write};

use expand_tilde::ExpandTilde;
use miette::Diagnostic;
use thiserror::Error;

use crate::config::path::DEFAULT;

#[derive(Debug, Error, Diagnostic)]
#[error("checking existence failed")]
#[diagnostic(
    code(melody::config::prepare::check_existence),
    help("make sure the permissions are set correctly")
)]
pub struct CheckExistsError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("creating directories failed")]
#[diagnostic(
    code(melody::config::prepare::create_dir_all),
    help("see the report for more information")
)]
pub struct CreateDirAllError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("write failed")]
#[diagnostic(
    code(melody::config::prepare::write),
    help("check that the path is accessible")
)]
pub struct WriteError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    ExpandTilde(#[from] expand_tilde::Error),
    CheckExists(#[from] CheckExistsError),
    CreateDirAll(#[from] CreateDirAllError),
    Write(#[from] WriteError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("writing the default config failed")]
#[diagnostic(
    code(melody::kit::config::defaults),
    help("make sure the `{DEFAULT}` can be created")
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

    pub fn expand(error: expand_tilde::Error) -> Self {
        Self::new(error.into())
    }

    pub fn check_exists(error: CheckExistsError) -> Self {
        Self::new(error.into())
    }

    pub fn create_dir_all(error: CreateDirAllError) -> Self {
        Self::new(error.into())
    }

    pub fn write(error: WriteError) -> Self {
        Self::new(error.into())
    }

    pub fn new_check_exists(error: std::io::Error) -> Self {
        Self::check_exists(CheckExistsError(error))
    }

    pub fn new_create_dir_all(error: std::io::Error) -> Self {
        Self::create_dir_all(CreateDirAllError(error))
    }

    pub fn new_write(error: std::io::Error) -> Self {
        Self::write(WriteError(error))
    }
}

pub const DEFAULT_STRING: &str = include_str!("default.toml");

pub fn prepare() -> Result<bool, Error> {
    let default_path = DEFAULT.expand_tilde_owned().map_err(Error::expand)?;

    if default_path.try_exists().map_err(Error::new_check_exists)? {
        return Ok(false);
    }

    if let Some(default_dir) = default_path.parent() {
        create_dir_all(default_dir).map_err(Error::new_create_dir_all)?;
    };

    write(default_path, DEFAULT_STRING).map_err(Error::new_write)?;

    Ok(true)
}
