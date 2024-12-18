update global self
set {
    clients += (
        select Client filter .id in array_unpack(<array<uuid>>$ids)
    )
};
