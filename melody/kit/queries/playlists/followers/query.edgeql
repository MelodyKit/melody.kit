select Playlist {
    followers: {
        id,
        name,
        follower_count,
        stream_count,
        stream_duration_ms,
        privacy_type,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    } offset <expression>$offset limit <expression>$limit
} filter .id = <uuid>$playlist_id;
