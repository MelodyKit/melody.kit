with
    result := (
        select fts::search(User, <str>$fts_query)
    ),
    users := (
        select result.object {
            id,
            name,
            private,
            follower_count,
            created_at,
            spotify_id,
            apple_music_id,
            yandex_music_id,
            discord_id,
        } order by result.score desc
    )
select users
filter is_user_accessible(users)
offset <expression>$offset limit <expression>$limit;
