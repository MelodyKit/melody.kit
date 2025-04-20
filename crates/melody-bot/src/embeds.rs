use melody_model::models::statistics::Statistics;
use rand::{Rng, rng};
use serenity::all::CreateEmbed;

use crate::format::tick;

pub const MELODY_PURPLE: u32 = 0xCC55FF;
pub const MELODY_BLUE: u32 = 0x55CCFF;

pub const HALF: f64 = 0.5;

pub fn melody_color() -> u32 {
    if rng().random_bool(HALF) {
        MELODY_PURPLE
    } else {
        MELODY_BLUE
    }
}

pub const INLINE: bool = true;

pub const ERROR: u32 = 0xFF0000;

pub const INTERNAL_ERROR: &str = "Internal Error";
pub const INTERNAL_ERROR_DESCRIPTION: &str =
    "An internal error occurred while processing the command.";

pub fn error_embed<E: std::error::Error>(_error: E) -> CreateEmbed {
    CreateEmbed::default()
        .title(INTERNAL_ERROR)
        .description(INTERNAL_ERROR_DESCRIPTION)
        .color(ERROR)
}

pub const STATISTICS: &str = "Statistics";

pub const USERS: &str = "Users";
pub const STREAMS: &str = "Streams";
pub const TRACKS: &str = "Tracks";
pub const ARTISTS: &str = "Artists";
pub const ALBUMS: &str = "Albums";
pub const PLAYLISTS: &str = "Playlists";

pub fn statistics_embed(statistics: &Statistics) -> CreateEmbed {
    CreateEmbed::new()
        .color(melody_color())
        .title(STATISTICS)
        .field(USERS, tick(statistics.user_count), INLINE)
        .field(STREAMS, tick(statistics.stream_count), INLINE)
        .field(TRACKS, tick(statistics.track_count), INLINE)
        .field(ARTISTS, tick(statistics.artist_count), INLINE)
        .field(ALBUMS, tick(statistics.album_count), INLINE)
        .field(PLAYLISTS, tick(statistics.playlist_count), INLINE)
}
