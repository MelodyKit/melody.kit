insert Album {
    artists := (
        for position_and_id in enumerate(array_unpack(<array<uuid>>$artist_ids)) union (
            select Artist {
                @position := position_and_id.0
            } filter .id = position_and_id.1
        )
    ),
    tracks := (
        for position_and_id in enumerate(array_unpack(<array<uuid>>$track_ids)) union (
            select Track {
                @position := position_and_id.0
            } filter .id = position_and_id.1
        )
    ),
    name := <str>$name,
    album_type := <AlbumType>$album_type,
    release_date := <date>$release_date,
    label := <str>$label,
};
