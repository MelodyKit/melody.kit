use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::UtcDateTime;
use melody_link::id::Id;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Entity<'e> {
    pub id: Id,
    pub created_at: UtcDateTime,
    pub name: CowStr<'e>,
    pub spotify_id: Option<CowStr<'e>>,
    pub apple_music_id: Option<CowStr<'e>>,
    pub yandex_music_id: Option<CowStr<'e>>,
}

impl fmt::Display for Entity<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.name.fmt(formatter)
    }
}

pub type StaticEntity = Entity<'static>;

impl IntoStatic for Entity<'_> {
    type Static = StaticEntity;

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
