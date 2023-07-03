update User
filter .id = <uuid>$user_id
set {
    following += (
        select User filter .id in array_unpack(<array<uuid>>$ids)
    )
};
