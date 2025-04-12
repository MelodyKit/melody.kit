use std::{fmt, str::FromStr};

use miette::Diagnostic;
use serde::{Deserialize, Deserializer, Serialize, Serializer, de};
use thiserror::Error;
use uuid::Uuid;

#[derive(Debug, Error, Diagnostic)]
#[error("invalid ID `{string}`")]
#[diagnostic(code(melody::shared::id), help("make sure the ID is valid"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: crate::uuid::Error,
    pub string: String,
}

impl Error {
    pub fn new(source: crate::uuid::Error, string: String) -> Self {
        Self { source, string }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
#[repr(transparent)]
pub struct Id {
    pub value: Uuid,
}

impl Serialize for Id {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        self.value.hyphenated().serialize(serializer)
    }
}

impl<'de> Deserialize<'de> for Id {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let string = <&str>::deserialize(deserializer)?;

        let id = string.parse().map_err(de::Error::custom)?;

        Ok(id)
    }
}

impl fmt::Display for Id {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.get().fmt(formatter)
    }
}

impl FromStr for Id {
    type Err = Error;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        let value =
            crate::uuid::parse(string).map_err(|error| Self::Err::new(error, string.to_owned()))?;

        Ok(Self::new(value))
    }
}

impl Id {
    pub const fn new(value: Uuid) -> Self {
        Self { value }
    }

    pub const fn get(self) -> Uuid {
        self.value
    }
}

impl From<Uuid> for Id {
    fn from(value: Uuid) -> Self {
        Self::new(value)
    }
}

impl From<Id> for Uuid {
    fn from(id: Id) -> Self {
        id.get()
    }
}
