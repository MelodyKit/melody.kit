//! Loading TOML files.
//!
//! The [`load`] function is used to load TOML files into values
//! of types that implement [`DeserializeOwned`].
//!
//! Parsing errors are rewrapped into [`ParseError`], and the [`struct@Error`] type
//! is used to handle all possible errors that can occur during loading.

use std::path::{Path, PathBuf};

use miette::Diagnostic;
use serde::de::DeserializeOwned;
use thiserror::Error;

use crate::{
    parse::{self, parse},
    read::{self, read},
};

/// Represents errors that can occur when parsing TOML at the given path.
#[derive(Debug, Error, Diagnostic)]
#[error("failed to parse TOML at `{path}`")]
#[diagnostic(
    code(melody::config::load::parse),
    help("see the report for more information")
)]
pub struct ParseError {
    /// The source of this error.
    #[source]
    #[diagnostic_source]
    pub source: parse::Error,

    /// The path to the file that was being parsed.
    pub path: PathBuf,
}

impl ParseError {
    /// Constructs [`Self`].
    pub fn new(source: parse::Error, path: PathBuf) -> Self {
        Self { source, path }
    }
}

/// Represents sources of errors that can occur during TOML loading.
#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    /// File error.
    Read(#[from] read::Error),
    /// Parse error.
    Parse(#[from] ParseError),
}

/// Represents errors that can occur when loading TOML files.
#[derive(Debug, Error, Diagnostic)]
#[error("failed to load TOML")]
#[diagnostic(
    code(melody::config::load),
    help("see the report for more information")
)]
pub struct Error {
    /// The source of this error.
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    /// Constructs [`Self`].
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    /// Constructs [`Self`] from [`read::Error`].
    pub fn read(error: read::Error) -> Self {
        Self::new(error.into())
    }

    /// Constructs [`Self`] from [`ParseError`].
    pub fn parse(error: ParseError) -> Self {
        Self::new(error.into())
    }
}

pub fn parse_aware<T: DeserializeOwned, S: AsRef<str>, P: AsRef<Path>>(
    string: S,
    path: P,
) -> Result<T, ParseError> {
    parse(string.as_ref()).map_err(|error| ParseError::new(error, path.as_ref().to_owned()))
}

/// Loads TOML from the given path into the value of specified or inferred type.
///
/// # Errors
///
/// Returns [`struct@Error`] if the file can not be read or its contents can not be parsed.
pub fn load<T: DeserializeOwned, P: AsRef<Path>>(path: P) -> Result<T, Error> {
    fn load_inner<T: DeserializeOwned>(path: &Path) -> Result<T, Error> {
        let string = read(path).map_err(Error::read)?;

        parse_aware(string, path).map_err(Error::parse)
    }

    load_inner(path.as_ref())
}
