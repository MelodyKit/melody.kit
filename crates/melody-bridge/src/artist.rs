use melody_model::models::artist::StaticArtist;
use melody_schema::{schema::artist::Artist as ArtistSchema, split::Split};
use miette::Diagnostic;
use thiserror::Error;

use crate::{
    bridge::{Bridge, TryBridge},
    entity, genres,
};

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Entity(#[from] entity::Error),
    Genres(#[from] genres::Error),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to bridge artist")]
#[diagnostic(code(melody::bridge::artist), help("check the schema for correctness"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub const fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn entity(error: entity::Error) -> Self {
        Self::new(error.into())
    }

    pub fn genres(error: genres::Error) -> Self {
        Self::new(error.into())
    }
}

impl TryBridge for ArtistSchema {
    type Model = StaticArtist;
    type Error = Error;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        let (common, specific) = self.split();

        let entity = common.try_bridge().map_err(Self::Error::entity)?;

        let follower_count = specific.follower_count.bridge();
        let stream_count = specific.stream_count.bridge();

        let genres = genres::try_bridge(specific.genres).map_err(Self::Error::genres)?;

        let model = Self::Model {
            entity,
            follower_count,
            stream_count,
            genres,
        };

        Ok(model)
    }
}
