use std::str::FromStr;

use bon::Builder;
use into_static::IntoStatic;
use miette::Diagnostic;
use non_empty_str::{CowStr, Empty};
use serde::{Deserialize, Serialize};
use thiserror::Error;

pub const SEPARATOR: &str = ":";

pub type Split<'s> = (&'s str, &'s str);

pub type Pair<'p> = (CowStr<'p>, CowStr<'p>);

#[derive(Debug, Error, Diagnostic)]
#[error("failed to split the pair due to format issues")]
#[diagnostic(
    code(melody::keyring::pairs::split),
    help("make sure the pair is formatted correctly and separated by `{SEPARATOR}`")
)]
pub struct SplitError;

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
pub enum ErrorSource {
    Split(#[from] SplitError),
    Empty(#[from] Empty),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to parse string into pair")]
#[diagnostic(
    code(melody::keyring::pair),
    help("make sure the pair is formatted correctly and separated by `{SEPARATOR}`")
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

    pub fn split(error: SplitError) -> Self {
        Self::new(error.into())
    }

    pub fn empty(error: Empty) -> Self {
        Self::new(error.into())
    }
}

pub fn split(string: &str) -> Result<Split<'_>, SplitError> {
    string.split_once(SEPARATOR).ok_or(SplitError)
}

pub fn split_pair(string: &str) -> Result<Pair<'_>, Error> {
    let (name_string, value_string) = split(string).map_err(Error::split)?;

    let name = CowStr::borrowed(name_string).map_err(Error::empty)?;
    let value = CowStr::borrowed(value_string).map_err(Error::empty)?;

    Ok((name, value))
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct UserPair<'u> {
    pub name: CowStr<'u>,
    pub password: CowStr<'u>,
}

impl<'u> UserPair<'u> {
    pub fn into_pair(self) -> Pair<'u> {
        (self.name, self.password)
    }
}

impl IntoStatic for UserPair<'_> {
    type Static = UserPair<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static {
            name: self.name.into_static(),
            password: self.password.into_static(),
        }
    }
}

impl<'p> From<Pair<'p>> for UserPair<'p> {
    fn from((name, password): Pair<'p>) -> Self {
        Self { name, password }
    }
}

impl<'u> From<UserPair<'u>> for Pair<'u> {
    fn from(user_pair: UserPair<'u>) -> Self {
        user_pair.into_pair()
    }
}

impl FromStr for UserPair<'_> {
    type Err = Error;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        let pair = split_pair(string)?.into_static();

        Ok(pair.into())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct ClientPair<'c> {
    pub id: CowStr<'c>,
    pub secret: CowStr<'c>,
}

impl<'c> ClientPair<'c> {
    pub fn into_pair(self) -> Pair<'c> {
        (self.id, self.secret)
    }
}

impl IntoStatic for ClientPair<'_> {
    type Static = ClientPair<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static {
            id: self.id.into_static(),
            secret: self.secret.into_static(),
        }
    }
}

impl<'p> From<Pair<'p>> for ClientPair<'p> {
    fn from((id, secret): Pair<'p>) -> Self {
        Self { id, secret }
    }
}

impl<'c> From<ClientPair<'c>> for Pair<'c> {
    fn from(client_pair: ClientPair<'c>) -> Self {
        client_pair.into_pair()
    }
}

impl FromStr for ClientPair<'_> {
    type Err = Error;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        let pair = split_pair(string)?.into_static();

        Ok(pair.into())
    }
}
