select User {
    id,
    verified,
    email,
    password_hash,
    secret
} filter .id = <uuid>$user_id;
