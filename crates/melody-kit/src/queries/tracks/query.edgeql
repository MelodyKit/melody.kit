select Track {
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
            genres,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id,
        },
        album_type,
        release_date,
        track_count,
        label,
        genres,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id,
    },
    artists: {
        id,
        name,
        follower_count,
        stream_count,
        genres,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id,
    },
    explicit,
    stream_count,
    genres,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id,
} filter .id = <uuid>$track_id;
