use bon::Builder;
use gel_derive::Queryable;
use melody_chrono::chrono::UtcDateTime;
use serde::{Deserialize, Serialize};

use crate::{
    schema::{album::Album, artist::Artist, entity::Entity},
    split::Split,
    types::{Count, Id},
};

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Track {
    pub id: Id,
    pub name: String,
    pub album: Album,
    pub artists: Vec<Artist>,
    pub explicit: bool,
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
    pub album: Album,
    pub artists: Vec<Artist>,
    pub explicit: bool,
    pub stream_count: Count,
    pub genres: Vec<String>,
}

impl Split for Track {
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
            album: self.album,
            artists: self.artists,
            explicit: self.explicit,
            stream_count: self.stream_count,
            genres: self.genres,
        };

        (common, specific)
    }
}
