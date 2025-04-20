use melody_model::models::statistics::Statistics;
use melody_schema::schema::statistics::Statistics as StatisticsSchema;

use crate::bridge::Bridge;

impl Bridge for StatisticsSchema {
    type Model = Statistics;

    fn bridge(self) -> Self::Model {
        Self::Model {
            track_count: self.track_count.bridge(),
            artist_count: self.artist_count.bridge(),
            album_count: self.album_count.bridge(),
            playlist_count: self.playlist_count.bridge(),
            user_count: self.user_count.bridge(),
            stream_count: self.stream_count.bridge(),
        }
    }
}
