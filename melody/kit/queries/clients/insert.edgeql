insert Client {
    name := <str>$name,
    description := <str>$description,
    secret_hash := <str>$secret_hash,
    creator := (select User filter .id = <uuid>$creator_id),
};
