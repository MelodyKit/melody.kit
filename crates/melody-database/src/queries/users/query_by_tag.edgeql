select User {
    id,
    tag,
    name,
    private,
    admin,
    follower_count,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id,
    discord_id,
} filter .tag = <str>$tag;
