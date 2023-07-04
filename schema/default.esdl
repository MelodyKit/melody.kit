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

    scalar type position extending int64 {
        constraint min_value(0);
    }

    scalar type expression extending int64 {
        constraint min_value(0);
    }

    abstract link with_position {
        property position -> position {
            default := 0;
        };
    }

    abstract link with_linked_at {
        property linked_at -> datetime {
            default := datetime_of_statement();
            readonly := true;
        };
    }

    abstract type Entity extending CreatedAt {
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

    type Track extending Entity, Genres {
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

    type Artist extending Entity, Genres {
        multi link followers := .<artists[is User];

        property follower_count := count(.followers);

        multi link streams := .<artists[is Track].<track[is Stream];

        property stream_count := count(.streams);
        property stream_duration_ms := sum(.streams.duration_ms);

        multi link tracks := .<artists[is Track];
        multi link albums := .<artists[is Album];

        property track_count := count(.tracks);  # used in queries
        property album_count := count(.albums);  # used in queries
    }

    type Album extending Entity, Genres {
        required multi link artists -> Artist;
        required multi link tracks extending with_position -> Track;

        required property album_type -> AlbumType {
            default := AlbumType.album;
        };

        required property release_date -> cal::local_date;

        property label -> str;

        property duration_ms := sum(.tracks.duration_ms);

        property track_count := count(.tracks);
    }

    type Playlist extending Entity {
        required link user -> User {
            on target delete delete source;
        };

        multi link followers := .<followed_playlists[is User];

        property follower_count := count(.followers);

        multi link tracks extending with_linked_at, with_position -> Track;

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

    type User extending Entity {
        multi link tracks extending with_linked_at -> Track;
        multi link albums extending with_linked_at -> Album;
        multi link artists extending with_linked_at -> Artist;

        multi link playlists := .<user[is Playlist];

        multi link following extending with_linked_at -> User;

        multi link followers := .<following[is User];

        multi link friends := (select .following filter .following in .followers);

        property following_count := count(.following);  # used in queries

        property follower_count := count(.followers);

        property friend_count := count(.friends);  # used in queries

        multi link followed_playlists extending with_linked_at -> Playlist;

        property followed_playlist_count := count(.followed_playlists);  # used in queries

        multi link streams := .<user[is Stream];

        property stream_count := count(.streams);
        property stream_duration_ms := sum(.streams.duration_ms);

        property track_count := count(.tracks);  # used in queries
        property album_count := count(.albums);  # used in queries
        property artist_count := count(.artists);  # used in queries
        property playlist_count := count(.playlists);  # used in queries

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
