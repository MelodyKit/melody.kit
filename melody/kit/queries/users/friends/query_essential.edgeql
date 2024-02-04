select User {
    friends: {
        id
    }
} filter .id = <uuid>$user_id;
