use bon::Builder;
use edgedb_tokio::Queryable;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::types::{SignedCount, UtcDateTime};

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct User {
    pub id: Uuid,
    pub tag: Option<String>,
    pub name: String,
    pub private: bool,
    pub follower_count: SignedCount,
    pub created_at: UtcDateTime,
    pub spotify_id: Option<String>,
    pub apple_music_id: Option<String>,
    pub yandex_music_id: Option<String>,
    pub discord_id: Option<String>,
}
