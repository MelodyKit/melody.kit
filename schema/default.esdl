module default {
    scalar type AlbumType extending enum<`album`, `single`, `compilation`>;
    scalar type PrivacyType extending enum<`public`, `friends`, `private`>;

    abstract type Base {
        required property name -> str;

        required property created_at -> datetime {
            default := datetime_current();
        };

        property spotify_id -> str;
        property apple_music_id -> bigint;
        property yandex_music_id -> bigint;
    }

    abstract type Genres {
        required property genres -> array<str> {
            default := <array<str>>[];
        };
    }

    type Track extending Base, Genres {
        required multi link artists -> Artist;

        required property explicit -> bool {
            default := false;
        };

        link album := assert_single(.<tracks[is Album]);
    }

    type Artist extending Base, Genres {
        multi link followers := .<artists[is User];

        property follower_count := count(.followers);

        multi link tracks := .<artists[is Track];
        multi link albums := .<artists[is Album];
    }

    type Album extending Base, Genres {
        required multi link artists -> Artist;
        required multi link tracks -> Track;

        required property album_type -> AlbumType {
            default := AlbumType.album;
        };

        required property release_date -> cal::local_date;

        property label -> str;

        property track_count := count(.tracks);
    }

    type Playlist extending Base {
        required link user -> User;
        multi link tracks -> Track;

        required property description -> str {
            default := "";
        };

        required property privacy_type -> PrivacyType {
            default := PrivacyType.public;
        };

        property track_count := count(.tracks);
    }

    type User extending Base {
        multi link tracks -> Track;
        multi link albums -> Album;
        multi link artists -> Artist;
        multi link playlists -> Playlist;

        multi link friends -> User;

        multi link followers -> User;

        property follower_count := count(.followers);

        required property verified -> bool {
            default := false;
        };

        required property privacy_type -> PrivacyType {
            default := PrivacyType.public;
        };

        required property email -> str {
            constraint exclusive;
        };
        required property password_hash -> str;
    }
}
