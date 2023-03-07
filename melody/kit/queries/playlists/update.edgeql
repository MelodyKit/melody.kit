update Playlist
filter .id = <uuid>$playlist_id
set {
    name := <str>$name,
    description := <str>$description,
    privacy_type := <PrivacyType>$privacy_type,
};
