update User
filter .id = <uuid>$user_id
set {
    name := <str>$name,
    explicit := <bool>$explicit,
    autoplay := <bool>$autoplay,
    platform := <Platform>$platform,
    privacy_type := <PrivacyType>$privacy_type,
};
