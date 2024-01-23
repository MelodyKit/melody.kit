module default {
    scalar type AlbumType extending enum<`album`, `single`, `compilation`>;
    scalar type PrivacyType extending enum<`public`, `friends`, `private`>;

    scalar type Platform extending enum<`any`, `spotify`, `apple_music`, `yandex_music`>;
    # scalar type Repeat extending enum <`none`, `context`, `one`>;

    abstract type CreatedAt {
        required created_at: datetime {
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

    # scalar type volume extending float64 {
    #     constraint min_value(0.0);
    #     constraint max_value(1.0);
    # }

    abstract link with_position {
        position: position {
            default := 0;
        };
    }

    abstract link with_linked_at {
        linked_at: datetime {
            default := datetime_of_statement();
            readonly := true;
        };
    }

    abstract type Entity extending CreatedAt {
        required name: str;

        spotify_id: str;
        apple_music_id: str;
        yandex_music_id: str;

        index fts::index on (
            fts::with_options(
                .name,
                language := fts::Language.eng,
                weight_category := fts::Weight.A,
            )
        );
    }

    abstract type Genres {
        required genres: array<str> {
            default := <array<str>>[];
        };
    }

    type Track extending Entity, Genres {
        required multi artists: Artist;

        required explicit: bool {
            default := false;
        };

        required duration_ms: duration_ms;

        multi streams := .<track[is Stream];

        stream_count := count(.streams);
        stream_duration_ms := sum(.streams.duration_ms);

        album := assert_single(.<tracks[is Album]);
    }

    type Artist extending Entity, Genres {
        multi followers := .<artists[is User];

        follower_count := count(.followers);

        multi streams := .<artists[is Track].<track[is Stream];

        stream_count := count(.streams);
        stream_duration_ms := sum(.streams.duration_ms);

        multi tracks := .<artists[is Track];
        multi albums := .<artists[is Album];

        track_count := count(.tracks);  # used in pagination
        album_count := count(.albums);  # used in pagination
    }

    type Album extending Entity, Genres {
        required multi artists: Artist;
        required multi tracks extending with_position: Track;

        required album_type: AlbumType {
            default := AlbumType.album;
        };

        required release_date: cal::local_date;

        label: str;

        duration_ms := sum(.tracks.duration_ms);

        track_count := count(.tracks);
    }

    type Playlist extending Entity {
        required user: User {
            on target delete delete source;
        };

        multi followers := .<followed_playlists[is User];

        follower_count := count(.followers);

        multi tracks extending with_linked_at, with_position: Track;

        description: str;

        required privacy_type: PrivacyType {
            default := PrivacyType.public;
        };

        duration_ms := sum(.tracks.duration_ms);

        track_count := count(.tracks);
    }

    type Stream extending CreatedAt {
        required user: User {
            on target delete delete source;
        };

        required track: Track {
            on target delete delete source;
        };

        required duration_ms: duration_ms;
    }

    # type PlayerSettings {
    #     required playing: bool {
    #         default := false;
    #     };
    #     required shuffle: bool {
    #         default := false;
    #     };
    #     required repeat: Repeat {
    #         default := Repeat.none;
    #     };
    #     required volume: volume {
    #         default := 0.5;
    #     };
    #     required volume_store: volume {
    #         default := 0.0;
    #     };
    # }

    type User extending Entity {
        multi tracks extending with_linked_at: Track;
        multi albums extending with_linked_at: Album;
        multi artists extending with_linked_at: Artist;

        multi playlists := .<user[is Playlist];

        multi following extending with_linked_at: User;

        multi followers := .<following[is User];

        multi friends := .following intersect .followers;

        following_count := count(.following);  # used in pagination

        follower_count := count(.followers);

        friend_count := count(.friends);  # used in pagination

        multi followed_playlists extending with_linked_at: Playlist;

        followed_playlist_count := count(.followed_playlists);  # used in pagination

        multi streams := .<user[is Stream];

        stream_count := count(.streams);
        stream_duration_ms := sum(.streams.duration_ms);

        track_count := count(.tracks);  # used in pagination
        album_count := count(.albums);  # used in pagination
        artist_count := count(.artists);  # used in pagination
        playlist_count := count(.playlists);  # used in pagination

        required verified: bool {
            default := false;
        };

        required premium: bool {
            default := false;
        }

        required explicit: bool {
            default := false;
        }

        required autoplay: bool {
            default := false;
        };

        required platform: Platform {
            default := Platform.any;
        };

        required privacy_type: PrivacyType {
            default := PrivacyType.public;
        };

        required email: str {
            constraint exclusive;
        };
        required password_hash: str;

        discord_id: str;

        spotify_token: str;
        apple_music_token: str;
        yandex_music_token: str;
    }
}
