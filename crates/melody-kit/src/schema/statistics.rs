use bon::Builder;
use edgedb_tokio::Queryable;
use serde::{Deserialize, Serialize};

use crate::types::SignedCount;

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Statistics {
    pub track_count: SignedCount,
    pub artist_count: SignedCount,
    pub album_count: SignedCount,
    pub playlist_count: SignedCount,
    pub user_count: SignedCount,
    pub stream_count: SignedCount,
}
