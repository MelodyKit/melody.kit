insert User {
    name := <str>$name,
    tag := <str>$tag,
    account := (select Account filter .id = <uuid>$account_id),
};
