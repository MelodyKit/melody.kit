select User {
    tracks: {
        id,
        name,
        album: {
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
            album_type,
            release_date,
            duration_ms,
            track_count,
            label,
            genres,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id
        },
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
    } order by @linked_at desc
} filter .id = <uuid>$user_id;