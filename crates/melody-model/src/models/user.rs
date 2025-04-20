use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_config::config::context::Context;
use melody_link::{
    entities::Type,
    links::{apple_music, linked::Linked, melody, spotify, yandex_music},
    locatable::Locatable,
    tag::Tag,
    uri::Uri,
};
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

use crate::{models::entity::Entity, types::Count};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct User<'u> {
    #[serde(flatten)]
    pub entity: Entity<'u>,
    pub tag: Option<Tag<'u>>,
    pub follower_count: Count,
    pub private: bool,
    pub admin: bool,
    pub discord_id: Option<CowStr<'u>>,
}

impl Linked for User<'_> {
    type Str = String;

    fn str(&self, context: &Context<'_>) -> Self::Str {
        melody::user(context, self.entity.id)
    }

    fn apple_music_str(&self) -> Option<Self::Str> {
        self.entity.apple_music_id.as_ref().map(apple_music::user)
    }

    fn spotify_str(&self) -> Option<Self::Str> {
        self.entity.spotify_id.as_ref().map(spotify::user)
    }

    fn yandex_music_str(&self) -> Option<Self::Str> {
        self.entity.yandex_music_id.as_ref().map(yandex_music::user)
    }
}

impl Locatable for User<'_> {
    fn uri(&self) -> Uri {
        Uri::new(Type::User, self.entity.id)
    }
}

impl fmt::Display for User<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.entity.fmt(formatter)
    }
}

pub type StaticUser = User<'static>;

impl IntoStatic for User<'_> {
    type Static = StaticUser;

    fn into_static(self) -> Self::Static {
        Self::Static {
            entity: self.entity.into_static(),
            tag: self.tag.into_static(),
            private: self.private,
            admin: self.admin,
            follower_count: self.follower_count,
            discord_id: self.discord_id.into_static(),
        }
    }
}
