use bon::Builder;
use serde::{Deserialize, Serialize};

use crate::{
    schema::statistics::Statistics as StatisticsSchema,
    types::{count, Count},
};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize, Builder)]
pub struct Statistics {
    pub track_count: Count,
    pub artist_count: Count,
    pub album_count: Count,
    pub playlist_count: Count,
    pub user_count: Count,
    pub stream_count: Count,
}

impl Statistics {
    pub fn from_schema(schema: StatisticsSchema) -> Self {
        Self {
            track_count: count(schema.track_count),
            artist_count: count(schema.artist_count),
            album_count: count(schema.album_count),
            playlist_count: count(schema.playlist_count),
            user_count: count(schema.user_count),
            stream_count: count(schema.stream_count),
        }
    }
}

impl From<StatisticsSchema> for Statistics {
    fn from(schema: StatisticsSchema) -> Self {
        Self::from_schema(schema)
    }
}
