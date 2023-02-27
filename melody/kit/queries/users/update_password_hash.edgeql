update User
filter .id = <uuid>$user_id
set {
    password_hash := <str>$password_hash
};
