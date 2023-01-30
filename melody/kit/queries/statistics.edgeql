select {
    track_count := count(Track),
    artist_count := count(Artist),
    album_count := count(Album),
    playlist_count := count(Playlist),
    user_count := count(User filter .verified),
    premium_user_count := count(User filter .premium),
};
