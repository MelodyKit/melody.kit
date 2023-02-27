update User
filter .id = <uuid>$user_id
set {
    artists += (
        select Artist filter .id in array_unpack(<array<str>>$ids)
    )
};
