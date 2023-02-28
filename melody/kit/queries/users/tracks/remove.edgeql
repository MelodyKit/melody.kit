update User
filter .id = <uuid>$user_id
set {
    tracks -= (
        select Track filter .id in array_unpack(<array<uuid>>$ids)
    )
};
