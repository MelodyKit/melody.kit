update User set {
    password_hash := <str>$password_hash
} filter .id = <uuid>$user_id;
