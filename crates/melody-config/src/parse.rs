//! Parsing TOML strings.
//!
//! This module simply wraps [`toml`] functionality to provide ergonomics an diagnostics.

use miette::Diagnostic;
use serde::de::DeserializeOwned;
use thiserror::Error;

/// Wraps [`toml::de::Error`] to provide diagnostics.
#[derive(Debug, Error, Diagnostic)]
#[error("failed to parse string into TOML")]
#[diagnostic(
    code(melody::config::parse),
    help("see the report for more information")
)]
pub struct Error(#[from] pub toml::de::Error);

pub fn parse<S: AsRef<str>, T: DeserializeOwned>(string: S) -> Result<T, Error> {
    toml::from_str(string.as_ref()).map_err(Error)
}
