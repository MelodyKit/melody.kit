
select User {
    friends: {
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
    } offset <expression>$offset limit <expression>$limit,
    friend_count
} filter .id = <uuid>$user_id;
