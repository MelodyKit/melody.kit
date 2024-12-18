use std::{borrow::Cow, fmt};

use bon::Builder;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::{cow, types::UtcDateTime};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Entity<'e> {
    pub id: Uuid,
    pub created_at: UtcDateTime,
    pub name: Cow<'e, str>,
    pub spotify_id: Option<Cow<'e, str>>,
    pub apple_music_id: Option<Cow<'e, str>>,
    pub yandex_music_id: Option<Cow<'e, str>>,
}

impl fmt::Display for Entity<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.name.fmt(formatter)
    }
}

pub type OwnedEntity = Entity<'static>;

impl Entity<'_> {
    pub fn into_owned(self) -> OwnedEntity {
        OwnedEntity {
            id: self.id,
            created_at: self.created_at,
            name: cow::into_owned(self.name),
            spotify_id: self.spotify_id.map(cow::into_owned),
            apple_music_id: self.apple_music_id.map(cow::into_owned),
            yandex_music_id: self.yandex_music_id.map(cow::into_owned),
        }
    }
}
