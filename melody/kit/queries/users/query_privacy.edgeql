select User {
    id,
    privacy_type,
} filter .id = <uuid>$user_id;
