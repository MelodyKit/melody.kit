module default {
    global current_user_id: uuid;

    global current_user := (
        select User filter .id = global current_user_id
    );

    # enums

    scalar type AlbumType extending enum<`album`, `single`, `compilation`>;
    scalar type PrivacyType extending enum<`public`, `friends`, `private`>;

    scalar type Platform extending enum<`any`, `spotify`, `apple_music`, `yandex_music`>;

    # scalars

    scalar type duration_ms extending int64 {
        constraint min_value(0);
    }

    scalar type position extending int64 {
        constraint min_value(0);
    }

    scalar type expression extending int64 {
        constraint min_value(0);
    }

    # abstract types

    abstract type Tracked {
        required created_at: datetime {
            default := datetime_of_statement();
            readonly := true;
        };
    }

    abstract type Named extending Tracked {
        required name: str;
    }

    abstract type Genres {
        required genres: array<str> {
            default := <array<str>>[];
        };
    }

    abstract type RedirectURLs {
        required redirect_urls: array<str> {
            default := <array<str>>[];
        };
    }

    # abstract links

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

    # entities

    abstract type Entity extending Named {
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

        track_count := count(.tracks);
        album_count := count(.albums);
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
        required owner: User {
            on target delete delete source;
            default := global current_user;
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

        access policy owner_has_full_access
            allow all
            using (global current_user ?= .owner);
    }

    type User extending Entity {
        multi tracks extending with_linked_at: Track;
        multi albums extending with_linked_at: Album;
        multi artists extending with_linked_at: Artist;

        multi playlists := .<owner[is Playlist];

        multi following extending with_linked_at: User;

        trigger forbid_follow_self after insert, update for each do (
            assert(
                not __new__ in __new__.following,
                message := "users can not follow themselves",
            )
        );

        multi followers := .<following[is User];

        multi friends := .following intersect .followers;

        following_count := count(.following);

        follower_count := count(.followers);

        friend_count := count(.friends);

        multi followed_playlists extending with_linked_at: Playlist;

        trigger forbid_follow_self_playlists after insert, update for each do (
            assert(
                not exists (__new__.playlists intersect __new__.followed_playlists),
                message := "users can not follow their own playlists",
            )
        );

        followed_playlist_count := count(.followed_playlists);

        multi streams := .<user[is Stream];

        stream_count := count(.streams);
        stream_duration_ms := sum(.streams.duration_ms);

        track_count := count(.tracks);
        album_count := count(.albums);
        artist_count := count(.artists);
        playlist_count := count(.playlists);

        required admin: bool {
            default := false;
        };

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

        secret: str;

        discord_id: str;

        multi clients extending with_linked_at: Client;
    }

    # non-entities

    type Stream extending Tracked {
        required user: User {
            on target delete delete source;
            default := global current_user;
        };

        required track: Track {
            on target delete delete source;
        };

        required duration_ms: duration_ms;
    }

    type Client extending Named, RedirectURLs {
        required owner: User {
            on target delete delete source;
            default := global current_user;
        };

        multi users := .<clients[is User];

        description: str;

        required secret_hash: str;

        access policy owner_has_full_access
            allow all
            using (global current_user ?= .owner);
    }
}
