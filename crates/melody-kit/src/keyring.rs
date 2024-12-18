use std::{borrow::Cow, str::FromStr};

use bon::Builder;
use keyring::Entry;
use miette::Diagnostic;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::{config::core::Keyring as KeyringConfig, cow};

#[derive(Debug, Error, Diagnostic)]
#[error("keyring find error")]
#[diagnostic(
    code(melody_kit::keyring::find),
    help("make sure the keyring is configured correctly")
)]
pub struct FindError(#[from] pub keyring::Error);

pub const SEPARATOR: &str = ":";

pub fn find<S: AsRef<str>, T: AsRef<str>>(service: S, name: T) -> Result<String, FindError> {
    fn find_inner(service: &str, name: &str) -> Result<String, FindError> {
        let string = Entry::new(service, name)?.get_password()?;

        Ok(string)
    }

    find_inner(service.as_ref(), name.as_ref())
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to parse `{string}` into pair")]
#[diagnostic(
    code(melody_kit::keyring::parse),
    help("make sure the pair is formatted correctly and separated by `{SEPARATOR}`")
)]
pub struct ParseError {
    pub string: String,
}

impl ParseError {
    pub fn new(string: String) -> Self {
        Self { string }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Pair<'p> {
    pub username: Cow<'p, str>,
    pub password: Cow<'p, str>,
}

impl<'p> Pair<'p> {
    pub fn new(username: Cow<'p, str>, password: Cow<'p, str>) -> Self {
        Self { username, password }
    }

    pub fn into_owned(self) -> Pair<'static> {
        Pair {
            username: cow::into_owned(self.username),
            password: cow::into_owned(self.password),
        }
    }
}

pub fn parse_pair(string: &str) -> Result<Pair<'_>, ParseError> {
    match string.split_once(SEPARATOR) {
        Some((username, password)) => {
            Ok(Pair::new(Cow::Borrowed(username), Cow::Borrowed(password)))
        }
        None => Err(ParseError::new(string.to_owned())),
    }
}

impl FromStr for Pair<'_> {
    type Err = ParseError;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        parse_pair(string).map(|pair| pair.into_owned())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct ClientPair<'p> {
    pub id: Cow<'p, str>,
    pub secret: Cow<'p, str>,
}

impl<'p> ClientPair<'p> {
    pub fn new(id: Cow<'p, str>, secret: Cow<'p, str>) -> Self {
        Self { id, secret }
    }

    pub fn into_owned(self) -> ClientPair<'static> {
        ClientPair {
            id: cow::into_owned(self.id),
            secret: cow::into_owned(self.secret),
        }
    }
}

pub fn parse_client_pair(string: &str) -> Result<ClientPair<'_>, ParseError> {
    match string.split_once(SEPARATOR) {
        Some((client_id, client_secret)) => Ok(ClientPair::new(
            Cow::Borrowed(client_id),
            Cow::Borrowed(client_secret),
        )),
        None => Err(ParseError::new(string.to_owned())),
    }
}

impl FromStr for ClientPair<'_> {
    type Err = ParseError;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        parse_client_pair(string).map(|pair| pair.into_owned())
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Find(#[from] FindError),
    Parse(#[from] ParseError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to load keyring")]
#[diagnostic(code(melody_kit::keyring), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn find(error: FindError) -> Self {
        Self::new(error.into())
    }

    pub fn parse(error: ParseError) -> Self {
        Self::new(error.into())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Keyring<'k> {
    pub bot: Cow<'k, str>,
    pub email: Pair<'k>,
    pub discord: ClientPair<'k>,
    pub spotify: ClientPair<'k>,
}

pub type OwnedKeyring = Keyring<'static>;

impl Keyring<'_> {
    pub fn into_owned(self) -> OwnedKeyring {
        OwnedKeyring {
            bot: cow::into_owned(self.bot),
            email: self.email.into_owned(),
            discord: self.discord.into_owned(),
            spotify: self.spotify.into_owned(),
        }
    }
}

impl Keyring<'_> {
    pub fn load_with(config: &KeyringConfig<'_>) -> Result<Self, Error> {
        let service = config.service.as_ref();

        let bot = find(service, config.bot.as_ref())
            .map(Cow::Owned)
            .map_err(Error::find)?;

        let email = find(service, config.email.as_ref())
            .map_err(Error::find)?
            .parse()
            .map_err(Error::parse)?;

        let discord = find(service, config.discord.as_ref())
            .map_err(Error::find)?
            .parse()
            .map_err(Error::parse)?;

        let spotify = find(service, config.spotify.as_ref())
            .map_err(Error::find)?
            .parse()
            .map_err(Error::parse)?;

        let keyring = Self::builder()
            .bot(bot)
            .email(email)
            .discord(discord)
            .spotify(spotify)
            .build();

        Ok(keyring)
    }
}
