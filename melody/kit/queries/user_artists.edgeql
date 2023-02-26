select User {
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
    } order by @linked_at desc
} filter .id = <uuid>$user_id;
