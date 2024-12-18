use std::{borrow::Cow, fmt};

use bon::Builder;
use serde::{Deserialize, Serialize};

use crate::{
    cow,
    enums::EntityType,
    models::entity::Entity,
    schema::user::User as UserSchema,
    types::{count, Count},
    uri::{Locatable, Uri},
};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct User<'u> {
    #[serde(flatten)]
    pub entity: Entity<'u>,
    pub tag: Option<Cow<'u, str>>,
    pub follower_count: Count,
    pub discord_id: Option<Cow<'u, str>>,
}

impl Locatable for User<'_> {
    fn uri(&self) -> Uri {
        Uri::new(EntityType::User, self.entity.id)
    }
}

impl fmt::Display for User<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.entity.fmt(formatter)
    }
}

impl User<'_> {
    pub fn from_schema(schema: UserSchema) -> Self {
        Self {
            entity: Entity {
                id: schema.id,
                created_at: schema.created_at,
                name: Cow::Owned(schema.name),
                spotify_id: schema.spotify_id.map(Cow::Owned),
                apple_music_id: schema.apple_music_id.map(Cow::Owned),
                yandex_music_id: schema.yandex_music_id.map(Cow::Owned),
            },
            tag: schema.tag.map(Cow::Owned),
            follower_count: count(schema.follower_count),
            discord_id: schema.discord_id.map(Cow::Owned),
        }
    }
}

impl From<UserSchema> for User<'_> {
    fn from(schema: UserSchema) -> Self {
        Self::from_schema(schema)
    }
}

pub type OwnedUser = User<'static>;

impl User<'_> {
    pub fn into_owned(self) -> OwnedUser {
        OwnedUser {
            entity: self.entity.into_owned(),
            tag: self.tag.map(cow::into_owned),
            follower_count: self.follower_count,
            discord_id: self.discord_id.map(cow::into_owned),
        }
    }
}
