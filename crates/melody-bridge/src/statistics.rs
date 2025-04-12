use std::convert::Infallible;

use melody_model::models::statistics::Statistics;
use melody_schema::schema::statistics::Statistics as StatisticsSchema;

use crate::bridge::Bridge;

impl Bridge for StatisticsSchema {
    type Model = Statistics;
    type Error = Infallible;

    fn bridge(self) -> Result<Self::Model, Self::Error> {
        let track_count = self.track_count.bridge()?;
        let artist_count = self.artist_count.bridge()?;
        let album_count = self.album_count.bridge()?;
        let playlist_count = self.playlist_count.bridge()?;
        let user_count = self.user_count.bridge()?;
        let stream_count = self.stream_count.bridge()?;

        let statistics = Self::Model::builder()
            .track_count(track_count)
            .artist_count(artist_count)
            .album_count(album_count)
            .playlist_count(playlist_count)
            .user_count(user_count)
            .stream_count(stream_count)
            .build();

        Ok(statistics)
    }
}
