select User {
} filter .id = <uuid>$user_id and .friends.id = <uuid>$target_id;
