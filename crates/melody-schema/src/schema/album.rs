use bon::Builder;
use gel_derive::Queryable;
use melody_chrono::chrono::{Date, UtcDateTime};
use serde::{Deserialize, Serialize};

use crate::{
    schema::{artist::Artist, entity::Entity},
    split::Split,
    types::{Count, Genres, Id},
};

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Album {
    pub id: Id,
    pub name: String,
    pub artists: Vec<Artist>,
    pub album_type: String,
    pub release_date: Date,
    pub track_count: Count,
    pub label: Option<String>,
    pub genres: Genres,
    pub created_at: UtcDateTime,
    pub spotify_id: Option<String>,
    pub apple_music_id: Option<String>,
    pub yandex_music_id: Option<String>,
}

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Specific {
    pub artists: Vec<Artist>,
    pub album_type: String,
    pub release_date: Date,
    pub track_count: Count,
    pub label: Option<String>,
    pub genres: Genres,
}

impl Split for Album {
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
            artists: self.artists,
            album_type: self.album_type,
            release_date: self.release_date,
            track_count: self.track_count,
            label: self.label,
            genres: self.genres,
        };

        (common, specific)
    }
}
