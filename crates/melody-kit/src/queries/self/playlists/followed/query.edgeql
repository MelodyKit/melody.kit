select global user {
    followed_playlists: {
        id,
        name,
        owner: {
            id,
            name,
            follower_count,
            stream_count,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id
            discord_id,
        },
        follower_count,
        description,
        track_count,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id,
    } order by @linked_at desc offset <expression>$offset limit <expression>$limit,
    followed_playlist_count,
};
