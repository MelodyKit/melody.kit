with result := (
    select fts::search(Album, <str>$fts_query)
) select result.object {
    id,
    name,
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
    },
    album_type,
    release_date,
    track_count,
    label,
    genres,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id,
} order by result.score desc offset <expression>$offset limit <expression>$limit;
