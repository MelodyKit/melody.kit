use std::{fmt, str::FromStr};

use miette::Diagnostic;
use serde::{Deserialize, Serialize};
use thiserror::Error;
use uuid::Uuid;

use crate::enums::EntityType;

pub const HEADER: &str = "melody.kit";
pub const SEPARATOR: &str = ":";

#[derive(Debug, Error, Diagnostic)]
#[error("unexpected EOF while parsing")]
#[diagnostic(code(melody_kit::uri::eof), help("make sure the string is valid"))]
pub struct EofError;

#[derive(Debug, Error, Diagnostic)]
#[error("invalid header `{string}`; expected `{HEADER}`")]
#[diagnostic(code(melody_kit::uri::header), help("make sure the header is valid"))]
pub struct HeaderError {
    pub string: String,
}

impl HeaderError {
    pub fn new(string: String) -> Self {
        Self { string }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("`{string}` is an invalid entity type")]
#[diagnostic(
    code(melody_kit::uri::entity_type),
    help("make sure the type is valid")
)]
pub struct EntityTypeError {
    pub string: String,
}

impl EntityTypeError {
    pub fn new(string: String) -> Self {
        Self { string }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("invalid UUID")]
#[diagnostic(code(melody_kit::uri::uuid), help("make sure the UUID is valid"))]
pub struct UuidError(#[from] pub uuid::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("`{string}` is an invalid ID")]
#[diagnostic(code(melody_kit::uri::id), help("make sure the ID is valid"))]
pub struct IdError {
    #[source]
    #[diagnostic_source]
    pub source: UuidError,
    pub string: String,
}

impl IdError {
    pub fn new(source: UuidError, string: String) -> Self {
        Self { source, string }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Eof(#[from] EofError),
    Header(#[from] HeaderError),
    EntityType(#[from] EntityTypeError),
    Id(#[from] IdError),
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

    pub fn new_header(header_string: String, string: String) -> Self {
        Self::header(HeaderError::new(header_string), string)
    }

    pub fn entity_type(error: EntityTypeError, string: String) -> Self {
        Self::new(error.into(), string)
    }

    pub fn new_entity_type(entity_type_string: String, string: String) -> Self {
        Self::entity_type(EntityTypeError::new(entity_type_string), string)
    }

    pub fn id(error: IdError, string: String) -> Self {
        Self::new(error.into(), string)
    }

    pub fn new_id(error: UuidError, id_string: String, string: String) -> Self {
        Self::id(IdError::new(error, id_string), string)
    }

    pub fn new_id_wrap(error: uuid::Error, id_string: String, string: String) -> Self {
        Self::new_id(UuidError(error), id_string, string)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Uri {
    pub entity_type: EntityType,
    pub id: Uuid,
}

impl Uri {
    pub fn new(entity_type: EntityType, id: Uuid) -> Self {
        Self { entity_type, id }
    }
}

impl FromStr for Uri {
    type Err = Error;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        if string.is_empty() {
            return Err(Self::Err::new_eof(string.to_owned()));
        }

        let mut split = string.split(SEPARATOR);

        let header = split
            .next()
            .ok_or_else(|| Self::Err::new_eof(string.to_owned()))?;

        if header != HEADER {
            return Err(Self::Err::new_header(header.to_owned(), string.to_owned()));
        };

        let string_type = split
            .next()
            .ok_or_else(|| Self::Err::new_eof(string.to_owned()))?;

        let entity_type = string_type
            .parse()
            .map_err(|_| Self::Err::new_entity_type(string_type.to_owned(), string.to_owned()))?;

        let string_id = split
            .next()
            .ok_or_else(|| Self::Err::new_eof(string.to_owned()))?;

        let id = string_id.parse().map_err(|error| {
            Self::Err::new_id_wrap(error, string_id.to_owned(), string.to_owned())
        })?;

        Ok(Self::new(entity_type, id))
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

pub trait Locatable {
    fn uri(&self) -> Uri;
}
