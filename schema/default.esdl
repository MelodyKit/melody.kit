module default {
    scalar type AlbumType extending enum<`album`, `single`, `compilation`>;
    scalar type PrivacyType extending enum<`public`, `friends`, `private`>;

    abstract type CreatedAt {
        required property created_at -> datetime {
            default := datetime_of_statement();
            readonly := true;
        };
    }

    scalar type duration_ms extending int64 {
        constraint min_value(0);
    }

    abstract type Base extending CreatedAt {
        required property name -> str;

        property spotify_id -> str;
        property apple_music_id -> str;
        property yandex_music_id -> str;
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

        required property duration_ms -> duration_ms;

        multi link streams := .<track[is Stream];

        property stream_count := count(.streams);
        property stream_duration_ms := sum(.streams.duration_ms);

        link album := assert_single(.<tracks[is Album]);
    }

    type Artist extending Base, Genres {
        multi link followers := .<artists[is User];

        property follower_count := count(.followers);

        multi link streams := .<artists[is Track].<track[is Stream];

        property stream_count := count(.streams);
        property stream_duration_ms := sum(.streams.duration_ms);

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

        property duration_ms := sum(.tracks.duration_ms);

        property track_count := count(.tracks);
    }

    type Playlist extending Base {
        required link user -> User {
            on target delete delete source;
        };

        multi link tracks -> Track;

        required property description -> str {
            default := "";
        };

        required property privacy_type -> PrivacyType {
            default := PrivacyType.public;
        };

        property duration_ms := sum(.tracks.duration_ms);

        property track_count := count(.tracks);
    }

    type Stream extending CreatedAt {
        required link user -> User {
            on target delete delete source;
        };

        required link track -> Track {
            on target delete delete source;
        };

        required property duration_ms -> duration_ms;
    }

    type User extending Base {
        multi link tracks -> Track;
        multi link albums -> Album;
        multi link artists -> Artist;

        multi link playlists := .<user[is Playlist];

        multi link friends -> User;

        multi link followers -> User;

        multi link following := .<followers[is User];

        property follower_count := count(.followers);

        multi link streams := .<user[is Stream].track;

        property stream_count := count(.streams);
        property stream_duration_ms := sum(.streams.duration_ms);

        required property verified -> bool {
            default := false;
        };

        required property premium -> bool {
            default := false;
        }

        required property privacy_type -> PrivacyType {
            default := PrivacyType.public;
        };

        required property email -> str {
            constraint exclusive;
        };
        required property password_hash -> str;
    }
}
