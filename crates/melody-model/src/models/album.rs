use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::Date;
use melody_config::config::context::Context;
use melody_enum::melody_enum;
use melody_link::{
    entities::Type,
    links::{apple_music, linked::Linked, melody, spotify, yandex_music},
    locatable::Locatable,
    uri::Uri,
};
use melody_vec::NonEmpty;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

use crate::{
    models::{artist::Artist, entity::Entity},
    types::Count,
};

melody_enum! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
    pub AlbumType {
        #[default]
        Album => album,
        Single => single,
        Compilation => compilation,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Album<'a> {
    pub entity: Entity<'a>,
    pub artists: NonEmpty<Artist<'a>>,
    pub album_type: AlbumType,
    pub release_date: Date,
    pub track_count: Count,
    pub label: Option<CowStr<'a>>,
    pub genres: Vec<CowStr<'a>>,
}

impl Linked for Album<'_> {
    type Str = String;

    fn str(&self, context: &Context<'_>) -> Self::Str {
        melody::album(context, self.entity.id)
    }

    fn apple_music_str(&self) -> Option<Self::Str> {
        self.entity.apple_music_id.as_ref().map(apple_music::album)
    }

    fn spotify_str(&self) -> Option<Self::Str> {
        self.entity.spotify_id.as_ref().map(spotify::album)
    }

    fn yandex_music_str(&self) -> Option<Self::Str> {
        self.entity
            .yandex_music_id
            .as_ref()
            .map(yandex_music::album)
    }
}

impl Locatable for Album<'_> {
    fn uri(&self) -> Uri {
        Uri::new(Type::Album, self.entity.id)
    }
}

impl fmt::Display for Album<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.entity.fmt(formatter)
    }
}

pub type StaticAlbum = Album<'static>;

impl IntoStatic for Album<'_> {
    type Static = StaticAlbum;

    fn into_static(self) -> Self::Static {
        Self::Static {
            entity: self.entity.into_static(),
            artists: self.artists.into_static(),
            album_type: self.album_type,
            release_date: self.release_date,
            track_count: self.track_count,
            label: self.label.into_static(),
            genres: self.genres.into_static(),
        }
    }
}
