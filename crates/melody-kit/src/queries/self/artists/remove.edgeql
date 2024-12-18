update global self
set {
    artists -= (
        select Artist filter .id in array_unpack(<array<uuid>>$ids)
    )
};
