update User
filter .id = <uuid>$user_id
set {
    albums -= (
        select Album filter .id in array_unpack(<array<uuid>>$ids)
    )
};
