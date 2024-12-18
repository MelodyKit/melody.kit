use melody_kit::{
    color::{MELODY_BLUE, MELODY_PURPLE},
    models::Statistics,
    types::Color,
};
use serenity::all::CreateEmbed;

pub const INTERNAL_ERROR: &str = "Internal Error";
pub const INTERNAL_ERROR_DESCRIPTION: &str =
    "An internal error occurred while processing the command.";
pub const INTERNAL_ERROR_COLOR: Color = 0xFF0000;

pub fn internal_error() -> CreateEmbed {
    CreateEmbed::default()
        .title(INTERNAL_ERROR)
        .description(INTERNAL_ERROR_DESCRIPTION)
        .color(INTERNAL_ERROR_COLOR)
}

pub const STATISTICS: &str = "Statistics";

pub const USERS: &str = "Users";
pub const STREAMS: &str = "Streams";
pub const TRACKS: &str = "Tracks";
pub const ARTISTS: &str = "Artists";
pub const ALBUMS: &str = "Albums";
pub const PLAYLISTS: &str = "Playlists";

pub fn statistics_embed(statistics: &Statistics, inline: bool) -> CreateEmbed {
    CreateEmbed::new()
        .title(STATISTICS)
        .field(USERS, statistics.user_count.to_string(), inline)
        .field(STREAMS, statistics.stream_count.to_string(), inline)
        .field(TRACKS, statistics.track_count.to_string(), inline)
        .field(ARTISTS, statistics.artist_count.to_string(), inline)
        .field(PLAYLISTS, statistics.playlist_count.to_string(), inline)
}

// def statistics_embed(statistics: Statistics, inline: bool = INLINE) -> Embed:
//     return (
//         Embed(color=choose_for_discord(), title=STATISTICS)
//         .add_field(name=USERS, value=count(statistics.user_count), inline=inline)
//         .add_field(name=STREAMS, value=count(statistics.stream_count), inline=inline)
//         .add_field(name=TRACKS, value=count(statistics.track_count), inline=inline)
//         .add_field(name=ARTISTS, value=count(statistics.artist_count), inline=inline)
//         .add_field(name=ALBUMS, value=count(statistics.album_count), inline=inline)
//         .add_field(name=PLAYLISTS, value=count(statistics.playlist_count), inline=inline)
//     )
