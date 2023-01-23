select User {
    artists: {
        id,
        name,
        follower_count,
        genres,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    }
} filter .id = <uuid>$user_id;
