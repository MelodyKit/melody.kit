module default {
    type Album extending Base {
        required property label -> str;
        required property release_date -> cal::local_date;
        required property genres -> array<str>;
        multi link tracks -> Track;
        property track_count := (select count(.tracks));
    }
}
