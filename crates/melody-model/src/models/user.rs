use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_config::config::context::Context;
use melody_link::{
    entities::Type,
    links::{apple_music, linked::Linked, melody, spotify, yandex_music},
    locatable::Locatable,
    tag::{self, Tag},
    uri::Uri,
};
use melody_schema::{schema::user::User as UserSchema, split::Split};
use miette::Diagnostic;
use non_empty_str::{CowStr, Empty};
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::{
    models::entity::{self, Entity},
    types::{
        Count, StaticCowStr, StaticTag, count_from_schema, owned_from_schema, tag_from_schema,
    },
};

#[derive(Debug, Error, Diagnostic)]
#[error("empty discord id encountered")]
#[diagnostic(code(melody::model::user::discord_id::empty))]
pub struct DiscordIdEmptyError(#[from] pub Empty);

pub fn discord_id_from_schema(
    schema: Option<String>,
) -> Result<Option<StaticCowStr>, DiscordIdEmptyError> {
    let discord_id = schema.map(owned_from_schema).transpose()?;

    Ok(discord_id)
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Entity(#[from] entity::Error),
    Tag(#[from] tag::Error),
    EmptyDiscordId(#[from] DiscordIdEmptyError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("user conversion failed")]
#[diagnostic(code(melody::model::user))]
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

    pub fn empty_discord_id(error: DiscordIdEmptyError) -> Self {
        Self::new(error.into())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct User<'u> {
    #[serde(flatten)]
    #[builder(into)]
    pub entity: Entity<'u>,
    #[builder(into)]
    pub tag: Option<Tag<'u>>,
    #[builder(into)]
    pub follower_count: Count,
    #[builder(into)]
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

impl IntoStatic for User<'_> {
    type Static = User<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static {
            entity: self.entity.into_static(),
            tag: self.tag.into_static(),
            follower_count: self.follower_count,
            discord_id: self.discord_id.into_static(),
        }
    }
}

pub fn optional_tag_from_schema(schema: Option<String>) -> Result<Option<StaticTag>, tag::Error> {
    let optional_tag = schema.map(tag_from_schema).transpose()?;

    Ok(optional_tag)
}

impl User<'_> {
    pub fn try_from_schema(schema: UserSchema) -> Result<Self, Error> {
        let (common, specific) = schema.split();

        let entity = Entity::try_from_schema(common).map_err(Error::entity)?;

        let tag = optional_tag_from_schema(specific.tag).map_err(Error::tag)?;

        let follower_count = count_from_schema(specific.follower_count);

        let discord_id =
            discord_id_from_schema(specific.discord_id).map_err(Error::empty_discord_id)?;

        let user = Self {
            entity,
            tag,
            follower_count,
            discord_id,
        };

        Ok(user)
    }
}
