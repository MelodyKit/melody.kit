update global self
set {
    tracks -= (
        select Track filter .id in array_unpack(<array<uuid>>$ids)
    )
};
