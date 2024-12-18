select Client {
    id,
    secret_hash,
    owner: {
        id
    },
} filter .id = <uuid>$client_id;
