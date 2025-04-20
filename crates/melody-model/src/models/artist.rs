use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_config::config::context::Context;
use melody_link::{
    entities::Type,
    links::{apple_music, linked::Linked, melody, spotify, yandex_music},
    locatable::Locatable,
    uri::Uri,
};
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

use crate::{models::entity::Entity, types::Count};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Artist<'a> {
    #[serde(flatten)]
    pub entity: Entity<'a>,
    pub follower_count: Count,
    pub stream_count: Count,
    pub genres: Vec<CowStr<'a>>,
}

impl Linked for Artist<'_> {
    type Str = String;

    fn str(&self, context: &Context<'_>) -> Self::Str {
        melody::artist(context, self.entity.id)
    }

    fn apple_music_str(&self) -> Option<Self::Str> {
        self.entity.apple_music_id.as_ref().map(apple_music::artist)
    }

    fn spotify_str(&self) -> Option<Self::Str> {
        self.entity.spotify_id.as_ref().map(spotify::artist)
    }

    fn yandex_music_str(&self) -> Option<Self::Str> {
        self.entity
            .yandex_music_id
            .as_ref()
            .map(yandex_music::artist)
    }
}

impl Locatable for Artist<'_> {
    fn uri(&self) -> Uri {
        Uri::new(Type::Artist, self.entity.id)
    }
}

impl fmt::Display for Artist<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.entity.fmt(formatter)
    }
}

pub type StaticArtist = Artist<'static>;

impl IntoStatic for Artist<'_> {
    type Static = StaticArtist;

    fn into_static(self) -> Self::Static {
        Self::Static {
            entity: self.entity.into_static(),
            follower_count: self.follower_count,
            stream_count: self.stream_count,
            genres: self.genres.into_static(),
        }
    }
}
