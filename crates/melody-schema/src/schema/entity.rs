use bon::Builder;
use gel_derive::Queryable;
use melody_chrono::chrono::UtcDateTime;
use serde::{Deserialize, Serialize};

use crate::types::Id;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Queryable, Builder)]
pub struct Entity {
    pub id: Id,
    pub name: String,
    pub created_at: UtcDateTime,
    pub spotify_id: Option<String>,
    pub apple_music_id: Option<String>,
    pub yandex_music_id: Option<String>,
}
