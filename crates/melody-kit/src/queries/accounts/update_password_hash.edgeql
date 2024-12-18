update Account
filter .id = <uuid>$account_id
set {
    password_hash := <uuid>$password_hash
};
