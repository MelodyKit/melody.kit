update User
filter .id = <uuid>$user_id
set {
    verified := <bool>$verified
};
