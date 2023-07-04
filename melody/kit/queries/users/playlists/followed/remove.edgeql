update User
filter .id = <uuid>$user_id
set {
    followed_playlists -= (select Playlist filter .id in array_unpack(<array<uuid>>$ids))
};
