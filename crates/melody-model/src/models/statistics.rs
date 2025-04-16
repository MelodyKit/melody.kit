use bon::Builder;
use melody_schema::schema::statistics::Statistics as StatisticsSchema;
use serde::{Deserialize, Serialize};

use crate::types::{Count, count_from_schema};

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
    pub const fn from_schema(schema: StatisticsSchema) -> Self {
        Self {
            track_count: count_from_schema(schema.track_count),
            artist_count: count_from_schema(schema.artist_count),
            album_count: count_from_schema(schema.album_count),
            playlist_count: count_from_schema(schema.playlist_count),
            user_count: count_from_schema(schema.user_count),
            stream_count: count_from_schema(schema.stream_count),
        }
    }
}

impl From<StatisticsSchema> for Statistics {
    fn from(schema: StatisticsSchema) -> Self {
        Self::from_schema(schema)
    }
}
