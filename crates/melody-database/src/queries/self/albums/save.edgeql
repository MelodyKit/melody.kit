update global self
set {
    albums += (
        select Album filter .id in array_unpack(<array<uuid>>$ids)
    )
};
