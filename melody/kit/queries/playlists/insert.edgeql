insert Playlist {
    name := <str>$name,
    description := <str>$description,
    privacy_type := <PrivacyType>$privacy_type,
    owner := (select User filter .id = <uuid>$owner_id),
};
