with
    result := (
        select fts::search(Playlist, <str>$fts_query)
    ),
    playlists := (
        select result.object {
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
                yandex_music_id,
                discord_id,
            },
            follower_count,
            description,
            track_count,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id,
        } order by result.score desc
    )
select playlists
filter is_playlist_accessible(playlists)
offset <expression>$offset limit <expression>$limit;
