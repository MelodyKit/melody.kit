use std::fmt;

use bon::Builder;
use into_static::IntoStatic;
use melody_chrono::chrono::UtcDateTime;
use melody_link::id::Id;
use non_empty_str::CowStr;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
pub struct Entity<'e> {
    #[builder(into)]
    pub id: Id,
    #[builder(into)]
    pub created_at: UtcDateTime,
    #[builder(into)]
    pub name: CowStr<'e>,
    #[builder(into)]
    pub spotify_id: Option<CowStr<'e>>,
    #[builder(into)]
    pub apple_music_id: Option<CowStr<'e>>,
    #[builder(into)]
    pub yandex_music_id: Option<CowStr<'e>>,
}

impl fmt::Display for Entity<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.name.fmt(formatter)
    }
}

impl IntoStatic for Entity<'_> {
    type Static = Entity<'static>;

    fn into_static(self) -> Self::Static {
        Self::Static::builder()
            .id(self.id)
            .created_at(self.created_at)
            .name(self.name.into_static())
            .maybe_spotify_id(self.spotify_id.into_static())
            .maybe_apple_music_id(self.apple_music_id.into_static())
            .maybe_yandex_music_id(self.yandex_music_id.into_static())
            .build()
    }
}
