select Client {
    id,
    name,
    owner: {
        id,
        name,
        created_at,
    },
    created_at,
    description,
} filter .id = <uuid>$client_id;
