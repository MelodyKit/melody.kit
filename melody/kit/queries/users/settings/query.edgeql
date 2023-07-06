select User {
    name,
    explicit,
    autoplay,
    platform,
    privacy_type
} filter .id = <uuid>$user_id;
