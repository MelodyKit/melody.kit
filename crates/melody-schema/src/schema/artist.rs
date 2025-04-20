use bon::Builder;
use gel_derive::Queryable;
use melody_chrono::UtcDateTime;
use serde::{Deserialize, Serialize};

use crate::{
    schema::entity::Entity,
    split::Split,
    types::{Count, Id},
};

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Artist {
    pub id: Id,
    pub name: String,
    pub follower_count: Count,
    pub stream_count: Count,
    pub genres: Vec<String>,
    pub created_at: UtcDateTime,
    pub spotify_id: Option<String>,
    pub apple_music_id: Option<String>,
    pub yandex_music_id: Option<String>,
}

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Specific {
    pub follower_count: Count,
    pub stream_count: Count,
    pub genres: Vec<String>,
}

impl Split for Artist {
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
            follower_count: self.follower_count,
            stream_count: self.stream_count,
            genres: self.genres,
        };

        (common, specific)
    }
}
