insert Client {
    name := <str>$name,
    secret_hash := <str>$secret_hash,
    creator := (select User filter .id = <uuid>$creator_id),
};
