module default {
    type Artist extending Base {
        multi link tracks := .<artists[is Track];
        required property genres -> array<str>;
    }
}
