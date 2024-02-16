select User {
    id,
    verified,
    email,
    password_hash,
    secret,
} filter .email = <str>$email;
