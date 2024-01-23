select Playlist {
    id,
    name,
    user: {
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
        discord_id
    },
    follower_count,
    description,
    duration_ms,
    track_count,
    privacy_type,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id
} filter .id = <uuid>$playlist_id;
