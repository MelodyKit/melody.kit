use bon::Builder;
use gel_derive::Queryable;
use melody_chrono::chrono::UtcDateTime;
use serde::{Deserialize, Serialize};

use crate::{
    schema::entity::Entity,
    split::Split,
    types::{Count, Id},
};

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct User {
    pub id: Id,
    pub tag: Option<String>,
    pub name: String,
    pub private: bool,
    pub follower_count: Count,
    pub created_at: UtcDateTime,
    pub spotify_id: Option<String>,
    pub apple_music_id: Option<String>,
    pub yandex_music_id: Option<String>,
    pub discord_id: Option<String>,
}

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Specific {
    pub tag: Option<String>,
    pub private: bool,
    pub follower_count: Count,
    pub discord_id: Option<String>,
}

impl Split for User {
    type Common = Entity;
    type Specific = Specific;

    fn split(self) -> (Self::Common, Self::Specific) {
        let common = Self::Common {
            id: self.id,
            name: self.name,
            created_at: self.created_at,
            spotify_id: self.spotify_id,
            apple_music_id: self.apple_music_id,
            yandex_music_id: self.yandex_music_id,
        };

        let specific = Self::Specific {
            tag: self.tag,
            private: self.private,
            follower_count: self.follower_count,
            discord_id: self.discord_id,
        };

        (common, specific)
    }
}
