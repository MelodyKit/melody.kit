use std::{fmt, str::FromStr};

use const_macros::const_early;
use miette::Diagnostic;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::{
    entities,
    id::{self, Id},
};

pub const HEADER: &str = "melody.kit";
pub const SEPARATOR: &str = ":";

#[derive(Debug, Error, Diagnostic)]
#[error("unexpected EOF while parsing URI")]
#[diagnostic(code(melody::shared::uri::eof), help("make sure the string is valid"))]
pub struct EofError;

#[derive(Debug, Error, Diagnostic)]
#[error("invalid header `{string}`; expected `{HEADER}`")]
#[diagnostic(
    code(melody::shared::uri::header),
    help("make sure the header is valid")
)]
pub struct HeaderError {
    pub string: String,
}

impl HeaderError {
    pub fn new(string: String) -> Self {
        Self { string }
    }
}

pub fn check_header<S: AsRef<str>>(string: S) -> Result<(), HeaderError> {
    fn check_header_inner(string: &str) -> Result<(), HeaderError> {
        const_early!(string != HEADER => HeaderError::new(string.to_owned()));

        Ok(())
    }

    check_header_inner(string.as_ref())
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Eof(#[from] EofError),
    Header(#[from] HeaderError),
    EntityType(#[from] entities::TypeError),
    Id(#[from] id::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to parse `{string}` to URI")]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
    pub string: String,
}

impl Error {
    pub fn new(source: ErrorSource, string: String) -> Self {
        Self { source, string }
    }

    pub fn eof(error: EofError, string: String) -> Self {
        Self::new(error.into(), string)
    }

    pub fn new_eof(string: String) -> Self {
        Self::eof(EofError, string)
    }

    pub fn header(error: HeaderError, string: String) -> Self {
        Self::new(error.into(), string)
    }

    pub fn entity_type(error: entities::TypeError, string: String) -> Self {
        Self::new(error.into(), string)
    }

    pub fn id(error: id::Error, string: String) -> Self {
        Self::new(error.into(), string)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Uri {
    pub entity_type: entities::Type,
    pub id: Id,
}

impl Uri {
    pub const fn new(entity_type: entities::Type, id: Id) -> Self {
        Self { entity_type, id }
    }
}

impl FromStr for Uri {
    type Err = Error;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        const_early!(string.is_empty() => Self::Err::new_eof(string.to_owned()));

        let mut split = string.split(SEPARATOR);

        let header = split
            .next()
            .ok_or_else(|| Self::Err::new_eof(string.to_owned()))?;

        check_header(header).map_err(|error| Self::Err::header(error, string.to_owned()))?;

        let string_type = split
            .next()
            .ok_or_else(|| Self::Err::new_eof(string.to_owned()))?;

        let entity_type = string_type
            .parse()
            .map_err(|error| Self::Err::entity_type(error, string.to_owned()))?;

        let string_id = split
            .next()
            .ok_or_else(|| Self::Err::new_eof(string.to_owned()))?;

        let id = string_id
            .parse()
            .map_err(|error| Self::Err::id(error, string.to_owned()))?;

        let uri = Self::new(entity_type, id);

        Ok(uri)
    }
}

impl fmt::Display for Uri {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(HEADER)?;

        formatter.write_str(SEPARATOR)?;

        self.entity_type.fmt(formatter)?;

        formatter.write_str(SEPARATOR)?;

        self.id.fmt(formatter)
    }
}
