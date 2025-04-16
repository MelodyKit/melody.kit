use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::UtcDateTime;
use melody_link::id::Id;
use melody_schema::schema::entity::Entity as EntitySchema;
use miette::Diagnostic;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::{string::owned_from_schema, types::id_from_schema};

#[derive(Debug, Error, Diagnostic)]
pub enum Error {
    #[error("empty name")]
    Name,
    #[error("empty spotify id")]
    SpotifyId,
    #[error("empty apple music id")]
    AppleMusicId,
    #[error("empty yandex music id")]
    YandexMusicId,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Entity<'e> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub created_at: UtcDateTime,
    #[builder(into)]
    pub name: CowStr<'e>,
    #[builder(into)]
    pub spotify_id: Option<CowStr<'e>>,
    #[builder(into)]
    pub apple_music_id: Option<CowStr<'e>>,
    #[builder(into)]
    pub yandex_music_id: Option<CowStr<'e>>,
}

impl fmt::Display for Entity<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.name.fmt(formatter)
    }
}

impl IntoStatic for Entity<'_> {
    type Static = Entity<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static {
            id: self.id,
            created_at: self.created_at,
            name: self.name.into_static(),
            spotify_id: self.spotify_id.into_static(),
            apple_music_id: self.apple_music_id.into_static(),
            yandex_music_id: self.yandex_music_id.into_static(),
        }
    }
}

impl Entity<'_> {
    pub fn try_from_schema(schema: EntitySchema) -> Result<Self, Error> {
        let id = id_from_schema(schema.id);
        let created_at = schema.created_at;

        let name = owned_from_schema(schema.name).map_err(|_| Error::Name)?;

        let spotify_id = schema
            .spotify_id
            .map(owned_from_schema)
            .transpose()
            .map_err(|_| Error::SpotifyId)?;

        let apple_music_id = schema
            .apple_music_id
            .map(owned_from_schema)
            .transpose()
            .map_err(|_| Error::AppleMusicId)?;

        let yandex_music_id = schema
            .yandex_music_id
            .map(owned_from_schema)
            .transpose()
            .map_err(|_| Error::YandexMusicId)?;

        let model = Self {
            id,
            created_at,
            name,
            spotify_id,
            apple_music_id,
            yandex_music_id,
        };

        Ok(model)
    }
}
