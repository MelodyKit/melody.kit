use bon::Builder;
use into_static::IntoStatic;
use non_empty_str::{CowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};

use crate::impl_default_with_builder;

pub const DEFAULT_SERVICE: CowStr<'static> = const_borrowed_str!("melody.kit");
pub const DEFAULT_SECRET: CowStr<'static> = const_borrowed_str!("secret");
pub const DEFAULT_EMAIL: CowStr<'static> = const_borrowed_str!("email");
pub const DEFAULT_BOT: CowStr<'static> = const_borrowed_str!("bot");
pub const DEFAULT_DISCORD: CowStr<'static> = const_borrowed_str!("discord");
pub const DEFAULT_SPOTIFY: CowStr<'static> = const_borrowed_str!("spotify");

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
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

impl IntoStatic for Keyring<'_> {
    type Static = Keyring<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .service(self.service.into_static())
            .email(self.email.into_static())
            .bot(self.bot.into_static())
            .discord(self.discord.into_static())
            .spotify(self.spotify.into_static())
            .build()
    }
}

impl_default_with_builder!(Keyring<'_>);
