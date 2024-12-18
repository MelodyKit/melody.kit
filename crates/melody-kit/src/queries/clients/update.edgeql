update Client
filter .id = <uuid>$client_id
set {
    name := <str>$name,
    description := <str>$description,
};
