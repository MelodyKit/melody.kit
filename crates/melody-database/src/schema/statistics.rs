use bon::Builder;
use gel_tokio::Queryable;
use serde::{Deserialize, Serialize};

use crate::types::Count;

#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Queryable, Builder,
)]
pub struct Statistics {
    pub track_count: Count,
    pub artist_count: Count,
    pub album_count: Count,
    pub playlist_count: Count,
    pub user_count: Count,
    pub stream_count: Count,
}
