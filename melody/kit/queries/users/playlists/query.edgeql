select User {
    playlists: {
        id,
        name,
        follower_count,
        description,
        duration_ms,
        track_count,
        privacy_type,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    } order by .created_at desc
} filter .id = <uuid>$user_id;
