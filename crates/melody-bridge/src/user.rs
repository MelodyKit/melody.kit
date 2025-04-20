use melody_link::tag::{self, Tag};
use melody_model::models::user::StaticUser;
use melody_schema::{schema::user::User as UserSchema, split::Split};
use miette::Diagnostic;
use non_empty_str::{CowStr, Empty};
use thiserror::Error;

use crate::{
    bridge::{Bridge, TryBridge},
    entity,
    macros::empty_error,
};

empty_error!(pub DiscordId @ "discord id" => "Discord ID");

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Entity(#[from] entity::Error),
    Tag(#[from] tag::Error),
    EmptyDiscordId(#[from] EmptyDiscordIdError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to bridge user")]
#[diagnostic(code(melody::bridge::user), help("check the schema for correctness"))]
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

    pub fn tag(error: tag::Error) -> Self {
        Self::new(error.into())
    }

    pub fn empty_discord_id(error: EmptyDiscordIdError) -> Self {
        Self::new(error.into())
    }

    pub fn new_empty_discord_id(error: Empty) -> Self {
        Self::empty_discord_id(error.into())
    }
}

impl TryBridge for UserSchema {
    type Model = StaticUser;
    type Error = Error;

    fn try_bridge(self) -> Result<Self::Model, Self::Error> {
        let (common, specific) = self.split();

        let entity = common.try_bridge().map_err(Error::entity)?;

        let tag = specific
            .tag
            .map(Tag::owned)
            .transpose()
            .map_err(Error::tag)?;

        let private = specific.private;
        let admin = specific.admin;

        let follower_count = specific.follower_count.bridge();

        let discord_id = specific
            .discord_id
            .try_bridge()
            .map_err(Error::new_empty_discord_id)?
            .map(CowStr::from_owned_str);

        let model = Self::Model {
            entity,
            tag,
            private,
            admin,
            follower_count,
            discord_id,
        };

        Ok(model)
    }
}
