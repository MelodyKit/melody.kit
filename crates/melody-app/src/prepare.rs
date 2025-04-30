use std::{
    env::set_current_dir,
    io::stderr,
    path::{Path, PathBuf},
};

use clap_verbosity_flag::{LogLevel, Verbosity};
use melody_config::prepare;
use miette::Diagnostic;
use thiserror::Error;
use tracing_subscriber::fmt;

#[derive(Debug, Error, Diagnostic)]
#[error("failed to change the current dir to `{path}`")]
#[diagnostic(
    code(melody::kit::prepare::change_current_dir),
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
#[error("failed to prepare tracing")]
#[diagnostic(
    code(melody::app::prepare::tracing),
    help("make sure tracing is not already initialized elsewhere")
)]
pub struct PrepareTracingError;

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    ChangeCurrentDir(#[from] ChangeCurrentDirError),
    PrepareTracing(#[from] PrepareTracingError),
    Prepare(#[from] prepare::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to prepare")]
#[diagnostic(
    code(melody::app::prepare),
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

    pub fn change_current_dir(error: ChangeCurrentDirError) -> Self {
        Self::new(error.into())
    }

    pub fn prepare(error: prepare::Error) -> Self {
        Self::new(error.into())
    }

    pub fn prepare_tracing(error: PrepareTracingError) -> Self {
        Self::new(error.into())
    }
}

pub fn change_current_dir<D: AsRef<Path>>(directory: D) -> Result<(), ChangeCurrentDirError> {
    fn change_current_dir_inner(directory: &Path) -> Result<(), ChangeCurrentDirError> {
        set_current_dir(directory)
            .map_err(|error| ChangeCurrentDirError::new(error, directory.to_owned()))
    }

    change_current_dir_inner(directory.as_ref())
}

pub fn prepare_tracing<L: LogLevel>(verbosity: Verbosity<L>) -> Result<(), PrepareTracingError> {
    fmt()
        .with_writer(stderr)
        .with_max_level(verbosity)
        .try_init()
        .map_err(|_| PrepareTracingError)?;

    Ok(())
}

pub fn prepare<D: AsRef<Path>, L: LogLevel>(
    directory: Option<D>,
    verbosity: Verbosity<L>,
) -> Result<(), Error> {
    if let Some(path) = directory {
        change_current_dir(path).map_err(Error::change_current_dir)?;
    };

    prepare_tracing(verbosity).map_err(Error::prepare_tracing)?;

    prepare::prepare().map_err(Error::prepare)?;

    Ok(())
}
