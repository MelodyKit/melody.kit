with user := (
    select User {
        albums: {
            id,
            name,
            artists: {
                id,
                name,
                follower_count,
                stream_count,
                stream_duration_ms,
                genres,
                created_at,
                spotify_id,
                apple_music_id,
                yandex_music_id
            },
            album_type,
            release_date,
            duration_ms,
            track_count,
            label,
            genres,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id
        } order by @linked_at desc offset <expression>$offset limit <expression>$limit,
        album_count
    } filter .id = <uuid>$user_id
)

select {
    items := user.albums,
    count := user.album_count
}
