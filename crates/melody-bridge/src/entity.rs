use melody_model::models::entity::StaticEntity;
use melody_schema::schema::entity::Entity as EntitySchema;
use miette::Diagnostic;
use non_empty_str::Empty;
use thiserror::Error;

use crate::{
    bridge::{Bridge, TryBridge},
    macros::empty_error,
};

empty_error!(pub Name @ "name" => "name");

empty_error!(pub SpotifyId @ "spotify id" => "Spotify ID");
empty_error!(pub AppleMusicId @ "apple music id" => "Apple Music ID");
empty_error!(pub YandexMusicId @ "yandex music id" => "Yandex Music ID");

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
#[error("failed to bridge entity")]
#[diagnostic(code(melody::bridge::entity), help("check the schema for correctness"))]
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

    pub fn new_empty_name(error: Empty) -> Self {
        Self::empty_name(error.into())
    }

    pub fn new_empty_spotify_id(error: Empty) -> Self {
        Self::empty_spotify_id(error.into())
    }

    pub fn new_empty_apple_music_id(error: Empty) -> Self {
        Self::empty_apple_music_id(error.into())
    }

    pub fn new_empty_yandex_music_id(error: Empty) -> Self {
        Self::empty_yandex_music_id(error.into())
    }
}

impl TryBridge for EntitySchema {
    type Model = StaticEntity;
    type Error = Error;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        let id = self.id.bridge();

        let name = self
            .name
            .try_bridge()
            .map_err(Self::Error::new_empty_name)?;

        let created_at = self.created_at;

        let spotify_id = self
            .spotify_id
            .try_bridge()
            .map_err(Self::Error::new_empty_spotify_id)?;

        let apple_music_id = self
            .apple_music_id
            .try_bridge()
            .map_err(Self::Error::new_empty_apple_music_id)?;

        let yandex_music_id = self
            .yandex_music_id
            .try_bridge()
            .map_err(Self::Error::new_empty_yandex_music_id)?;

        let model = Self::Model {
            id,
            name,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id,
        };

        Ok(model)
    }
}
