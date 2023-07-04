select Album {
    tracks: {
        id,
        name,
        artists: {
            id,
            name,
            follower_count,
            stream_count,
            stream_duration_ms,
            genres,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id
        },
        explicit,
        duration_ms,
        stream_count,
        stream_duration_ms,
        genres,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    } order by @position offset <expression>$offset limit <expression>$limit,
    track_count
} filter .id = <uuid>$album_id;
