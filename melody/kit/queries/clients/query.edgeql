select Client {
    id,
    name,
    secret_hash,
    creator: {
        id,
        name,
        created_at,
    },
    created_at,
} filter .id = <uuid>$client_id;
