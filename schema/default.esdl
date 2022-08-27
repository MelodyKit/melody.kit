module default {
    type Base {
        required property name -> str;
        required property image -> str;

        required property created_at -> datetime {
            default := datetime_current();
            readonly := true;
        };

        property spotify_id -> str;
        property apple_music_id -> bigint;
        property yandex_music_id -> bigint;
    }

    type Track extending Base {
        required multi link artists -> Artist;

        multi link albums := .<tracks[is Album];
    }

    type Artist extending Base {
        required property genres -> array<str>;

        multi link tracks := .<artists[is Track];
        multi link albums := .<artists[is Album];
    }

    type Album extending Base {
        required multi link artists -> Artist;
        required multi link tracks -> Track;

        required property album_type -> str;
        required property release_date -> cal::local_date;
        required property genres -> array<str>;

        required property label -> str;

        property track_count := (select count(.tracks));
    }

    type Playlist extending Base {
        required link user -> User;
        multi link tracks -> Track;
    }

    type User extending Base {
        required property email -> str {
            constraint exclusive;
        };
        required property password -> str;
    }
}
