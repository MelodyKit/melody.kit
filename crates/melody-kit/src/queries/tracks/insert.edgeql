insert Track {
    artists := (
        for position_and_id in enumerate(array_unpack(<array<uuid>>$artist_ids)) union (
            select Artist {
                @position := position_and_id.0
            } filter .id = position_and_id.1
        )
    ),
    name := <str>$name,
    explicit := <bool>$explicit,
};
