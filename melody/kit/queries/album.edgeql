select Album {
    id,
    name,
    artists: {
        id,
        name,
        follower_count,
        genres,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    },
    album_type,
    release_date,
    track_count,
    label,
    genres,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id
} filter .id = <uuid>$album_id;
