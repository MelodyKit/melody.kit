use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, StaticCowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::impl_default_with_builder;

pub const DEFAULT_SERVICE: StaticCowStr = const_borrowed_str!("melody.kit");
pub const DEFAULT_SECRET: StaticCowStr = const_borrowed_str!("secret");
pub const DEFAULT_EMAIL: StaticCowStr = const_borrowed_str!("email");
pub const DEFAULT_BOT: StaticCowStr = const_borrowed_str!("bot");
pub const DEFAULT_DISCORD: StaticCowStr = const_borrowed_str!("discord");
pub const DEFAULT_SPOTIFY: StaticCowStr = const_borrowed_str!("spotify");

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Builder)]
#[serde(default, rename_all = "kebab-case")]
pub struct Keyring<'k> {
    #[builder(default = DEFAULT_SERVICE)]
    pub service: CowStr<'k>,

    #[builder(default = DEFAULT_SECRET)]
    pub secret: CowStr<'k>,

    #[builder(default = DEFAULT_EMAIL)]
    pub email: CowStr<'k>,

    #[builder(default = DEFAULT_BOT)]
    pub bot: CowStr<'k>,

    #[builder(default = DEFAULT_DISCORD)]
    pub discord: CowStr<'k>,

    #[builder(default = DEFAULT_SPOTIFY)]
    pub spotify: CowStr<'k>,
}

pub type StaticKeyring = Keyring<'static>;

impl IntoStatic for Keyring<'_> {
    type Static = StaticKeyring;

    fn into_static(self) -> Self::Static {
        Self::Static {
            service: self.service.into_static(),
            secret: self.secret.into_static(),
            email: self.email.into_static(),
            bot: self.bot.into_static(),
            discord: self.discord.into_static(),
            spotify: self.spotify.into_static(),
        }
    }
}

impl_default_with_builder!(Keyring<'_>);
