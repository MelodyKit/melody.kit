select User {
    id,
    name,
    follower_count,
    stream_count,
    stream_duration_ms,
    privacy_type,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id,
    discord_id,
} filter .discord_id = <str>$discord_id;
