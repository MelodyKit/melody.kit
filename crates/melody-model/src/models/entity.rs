use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::UtcDateTime;
use melody_link::id::Id;
use melody_schema::schema::entity::Entity as EntitySchema;
use miette::Diagnostic;
use non_empty_str::{CowStr, Empty};
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::types::{StaticCowStr, id_from_schema, owned_from_schema};

#[derive(Debug, Error, Diagnostic)]
#[error("empty name encountered")]
#[diagnostic(code(melody::model::entity::name::empty))]
pub struct EmptyNameError(#[from] pub Empty);

pub fn name_from_schema(schema: String) -> Result<StaticCowStr, EmptyNameError> {
    let name = owned_from_schema(schema)?;

    Ok(name)
}

#[derive(Debug, Error, Diagnostic)]
#[error("empty spotify id encountered")]
#[diagnostic(code(melody::model::entity::spotify_id::empty))]
pub struct EmptySpotifyIdError(#[from] pub Empty);

pub fn spotify_id_from_schema(
    schema: Option<String>,
) -> Result<Option<StaticCowStr>, EmptySpotifyIdError> {
    let spotify_id = schema.map(owned_from_schema).transpose()?;

    Ok(spotify_id)
}

#[derive(Debug, Error, Diagnostic)]
#[error("empty apple music id encountered")]
#[diagnostic(code(melody::model::entity::apple_music_id::empty))]
pub struct EmptyAppleMusicIdError(#[from] pub Empty);

pub fn apple_music_id_from_schema(
    schema: Option<String>,
) -> Result<Option<StaticCowStr>, EmptyAppleMusicIdError> {
    let apple_music_id = schema.map(owned_from_schema).transpose()?;

    Ok(apple_music_id)
}

#[derive(Debug, Error, Diagnostic)]
#[error("empty yandex music id encountered")]
#[diagnostic(code(melody::model::entity::yandex_music_id::empty))]
pub struct EmptyYandexMusicIdError(#[from] pub Empty);

pub fn yandex_music_id_from_schema(
    schema: Option<String>,
) -> Result<Option<StaticCowStr>, EmptyYandexMusicIdError> {
    let yandex_music_id = schema.map(owned_from_schema).transpose()?;

    Ok(yandex_music_id)
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    EmptyName(#[from] EmptyNameError),
    EmptySpotifyId(#[from] EmptySpotifyIdError),
    EmptyAppleMusicId(#[from] EmptyAppleMusicIdError),
    EmptyYandexMusicId(#[from] EmptyYandexMusicIdError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("entity conversion failed")]
#[diagnostic(code(melody::model::entity))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub const fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn empty_name(error: EmptyNameError) -> Self {
        Self::new(error.into())
    }

    pub fn empty_spotify_id(error: EmptySpotifyIdError) -> Self {
        Self::new(error.into())
    }

    pub fn empty_apple_music_id(error: EmptyAppleMusicIdError) -> Self {
        Self::new(error.into())
    }

    pub fn empty_yandex_music_id(error: EmptyYandexMusicIdError) -> Self {
        Self::new(error.into())
    }
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

        let name = name_from_schema(schema.name).map_err(Error::empty_name)?;

        let spotify_id =
            spotify_id_from_schema(schema.spotify_id).map_err(Error::empty_spotify_id)?;

        let apple_music_id = apple_music_id_from_schema(schema.apple_music_id)
            .map_err(Error::empty_apple_music_id)?;

        let yandex_music_id = yandex_music_id_from_schema(schema.yandex_music_id)
            .map_err(Error::empty_yandex_music_id)?;

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
