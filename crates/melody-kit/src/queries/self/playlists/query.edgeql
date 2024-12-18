select global self {
    playlists: {
        id,
        name,
        follower_count,
        description,
        track_count,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id,
    } order by .created_at desc offset <expression>$offset limit <expression>$limit,
    playlist_count,
};
