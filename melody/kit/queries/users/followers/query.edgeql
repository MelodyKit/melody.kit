select User {
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
        yandex_music_id,
        discord_id
    } order by @linked_at desc offset <expression>$offset limit <expression>$limit,
    follower_count
} filter .id = <uuid>$user_id;
