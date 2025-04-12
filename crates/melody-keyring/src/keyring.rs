use bon::Builder;
use into_static::IntoStatic;
use miette::Diagnostic;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use melody_config::config::keyring::Keyring as KeyringConfig;

use crate::{
    find::{self, find},
    pairs::{self, ClientPair, UserPair},
};

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Find(#[from] find::Error),
    Pairs(#[from] pairs::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to load keyring")]
#[diagnostic(
    code(melody::keyring::keyring),
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

    pub fn find(error: find::Error) -> Self {
        Self::new(error.into())
    }

    pub fn pairs(error: pairs::Error) -> Self {
        Self::new(error.into())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Keyring<'k> {
    #[builder(into)]
    pub bot: CowStr<'k>,
    #[builder(into)]
    pub email: UserPair<'k>,
    #[builder(into)]
    pub discord: ClientPair<'k>,
    #[builder(into)]
    pub spotify: ClientPair<'k>,
}

impl IntoStatic for Keyring<'_> {
    type Static = Keyring<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .bot(self.bot.into_static())
            .email(self.email.into_static())
            .discord(self.discord.into_static())
            .spotify(self.spotify.into_static())
            .build()
    }
}

impl Keyring<'_> {
    pub fn load_with(config: &KeyringConfig<'_>) -> Result<Self, Error> {
        let service = config.service.as_ref();

        let bot = find(service, config.bot.as_ref()).map_err(Error::find)?;

        let email: UserPair<'_> = find(service, config.email.as_ref())
            .map_err(Error::find)?
            .parse()
            .map_err(Error::pairs)?;

        let discord: ClientPair<'_> = find(service, config.discord.as_ref())
            .map_err(Error::find)?
            .parse()
            .map_err(Error::pairs)?;

        let spotify: ClientPair<'_> = find(service, config.spotify.as_ref())
            .map_err(Error::find)?
            .parse()
            .map_err(Error::pairs)?;

        let keyring = Self::builder()
            .bot(bot)
            .email(email)
            .discord(discord)
            .spotify(spotify)
            .build();

        Ok(keyring)
    }
}
