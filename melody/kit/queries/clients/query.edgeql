select Client {
    id,
    name,
    creator: {
        id,
        name,
        created_at,
    },
    created_at,
    description,
} filter .id = <uuid>$client_id;
