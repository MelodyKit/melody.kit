with result := (
    select fts::search(Playlist, <str>$fts_query)
) select result.object {
    id,
    name,
    user: {
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
        discord_id,
    },
    follower_count,
    description,
    duration_ms,
    track_count,
    privacy_type,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id,
} order by result.score desc offset <expression>$offset limit <expression>$limit;
