select Playlist {
    id,
    privacy_type,
    owner: {
        id,
        privacy_type,
    },
} filter .id = <uuid>$playlist_id;
