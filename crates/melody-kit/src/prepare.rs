use std::{
    env::set_current_dir,
    path::{Path, PathBuf},
};

use miette::Diagnostic;
use thiserror::Error;

use crate::config::default::default_write;

#[derive(Debug, Error, Diagnostic)]
#[error("failed to change the current dir to `{path}`")]
#[diagnostic(
    code(melody_kit::prepare::change_current_dir),
    help("check whether the directory exists and is accessible")
)]
pub struct ChangeCurrentDirError {
    pub source: std::io::Error,
    pub path: PathBuf,
}

impl ChangeCurrentDirError {
    pub fn new(source: std::io::Error, path: PathBuf) -> Self {
        Self { source, path }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    ChangeCurrentDir(#[from] ChangeCurrentDirError),
    Default(#[from] crate::config::default::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to prepare")]
#[diagnostic(code(melody_kit::prepare), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn change_current_dir(error: ChangeCurrentDirError) -> Self {
        Self::new(error.into())
    }

    pub fn default(error: crate::config::default::Error) -> Self {
        Self::new(error.into())
    }

    pub fn new_change_current_dir(error: std::io::Error, path: PathBuf) -> Self {
        Self::change_current_dir(ChangeCurrentDirError::new(error, path))
    }
}

pub fn prepare<D: AsRef<Path>>(directory: Option<D>) -> Result<(), Error> {
    if let Some(path) = directory {
        let path = path.as_ref();

        set_current_dir(path)
            .map_err(|error| Error::new_change_current_dir(error, path.to_owned()))?;
    }

    default_write().map_err(Error::default)?;

    Ok(())
}
