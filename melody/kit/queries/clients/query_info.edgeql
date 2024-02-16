select Client {
    id,
    secret_hash,
    creator: {
        id
    },
} filter .id = <uuid>$client_id;
