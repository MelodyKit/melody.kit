select User {
    id,
    verified,
    email,
    password_hash,
} filter .email = <str>$email;
