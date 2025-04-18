select global self {
    friends: {
        id,
        name,
        follower_count,
        stream_count,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id,
        discord_id,
    } offset <expression>$offset limit <expression>$limit,
    friend_count,
};
