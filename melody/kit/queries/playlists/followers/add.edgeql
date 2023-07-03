update Playlist
filter .id = <uuid>$playlist_id
set {
    followers += (select User filter .id = <uuid>$user_id)
};