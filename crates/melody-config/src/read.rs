//! Reading files to strings.

use std::{
    fs::read_to_string,
    path::{Path, PathBuf},
};

use miette::Diagnostic;
use thiserror::Error;

/// Represents errors that can occur when reading files to strings.
#[derive(Debug, Error, Diagnostic)]
#[error("failed to read file at `{path}`")]
#[diagnostic(code(melody::config::read), help("make sure the file is accessible"))]
pub struct Error {
    /// The underlying I/O error.
    pub source: std::io::Error,
    /// The path provided.
    pub path: PathBuf,
}

impl Error {
    /// Constructs [`Self`].
    pub fn new(source: std::io::Error, path: PathBuf) -> Self {
        Self { source, path }
    }
}

/// Reads the file at the provided path.
///
/// # Errors
///
/// Returns [`struct@Error`] if any I/O errors occur during reading.
pub fn read<P: AsRef<Path>>(path: P) -> Result<String, Error> {
    fn read_inner(path: &Path) -> Result<String, Error> {
        read_to_string(path).map_err(|error| Error::new(error, path.to_owned()))
    }

    read_inner(path.as_ref())
}
