update User
filter .id = <uuid>$user_id
set {
    clients += (select Client filter .id = <uuid>$client_id)
};
