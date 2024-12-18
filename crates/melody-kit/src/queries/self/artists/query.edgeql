select global self {
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
    } order by @linked_at desc offset <expression>$offset limit <expression>$limit,
    artist_count,
};
