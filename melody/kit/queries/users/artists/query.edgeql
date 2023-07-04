with user := (
    select User {
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
        } order by @linked_at desc offset <expression>$offset limit <expression>$limit,
        artist_count
    } filter .id = <uuid>$user_id
)

select {
    items := user.artists,
    count := user.artist_count
}
