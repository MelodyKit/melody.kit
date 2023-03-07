insert Playlist {
    name := <str>$name,
    description := <str>$description,
    privacy_type := <PrivacyType>$privacy_type,
    user := (select User filter .id = <uuid>$user_id),
};
