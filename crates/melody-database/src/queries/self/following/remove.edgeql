update global self
set {
    following -= (
        select User filter .id in array_unpack(<array<uuid>>$ids)
    )
};
