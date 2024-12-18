select Account {
    id,
    created_at,
    email,
    password_hash,
    secret,
    user: {
        id
    },
    admin,
    premium,
} filter .email = <str>$email;
