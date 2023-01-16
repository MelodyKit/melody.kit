CREATE MIGRATION m1olrbnx3kxjd3evmp6m6ub2az3xqawzd7lya2rx7llrmpkf3ei5ma
    ONTO initial
{
  CREATE FUTURE nonrecursive_access_policies;
  CREATE ABSTRACT TYPE default::Base {
      CREATE PROPERTY apple_music_id -> std::bigint;
      CREATE REQUIRED PROPERTY created_at -> std::datetime {
          SET default := (SELECT
              std::datetime_current()
          );
      };
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE PROPERTY spotify_id -> std::str;
      CREATE PROPERTY yandex_music_id -> std::bigint;
  };
  CREATE ABSTRACT TYPE default::Genres {
      CREATE REQUIRED PROPERTY genres -> array<std::str> {
          SET default := (<array<std::str>>[]);
      };
  };
  CREATE SCALAR TYPE default::AlbumType EXTENDING enum<album, `single`, compilation>;
  CREATE TYPE default::Album EXTENDING default::Base, default::Genres {
      CREATE REQUIRED PROPERTY album_type -> default::AlbumType;
      CREATE REQUIRED PROPERTY label -> std::str;
      CREATE REQUIRED PROPERTY release_date -> cal::local_date;
  };
  CREATE TYPE default::Artist EXTENDING default::Base, default::Genres;
  ALTER TYPE default::Album {
      CREATE REQUIRED MULTI LINK artists -> default::Artist;
  };
  ALTER TYPE default::Artist {
      CREATE MULTI LINK albums := (.<artists[IS default::Album]);
  };
  CREATE TYPE default::Track EXTENDING default::Base, default::Genres {
      CREATE REQUIRED MULTI LINK artists -> default::Artist;
      CREATE REQUIRED PROPERTY explicit -> std::bool {
          SET default := false;
      };
  };
  ALTER TYPE default::Album {
      CREATE REQUIRED MULTI LINK tracks -> default::Track;
      CREATE PROPERTY track_count := (SELECT
          std::count(.tracks)
      );
  };
  ALTER TYPE default::Track {
      CREATE LINK album := (std::assert_single(.<tracks[IS default::Album]));
  };
  CREATE TYPE default::User EXTENDING default::Base {
      CREATE MULTI LINK albums -> default::Album;
      CREATE MULTI LINK artists -> default::Artist;
      CREATE MULTI LINK tracks -> default::Track;
      CREATE REQUIRED PROPERTY email -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY password_hash -> std::str;
  };
  ALTER TYPE default::Artist {
      CREATE MULTI LINK tracks := (.<artists[IS default::Track]);
  };
  CREATE TYPE default::Playlist EXTENDING default::Base {
      CREATE MULTI LINK tracks -> default::Track;
      CREATE REQUIRED LINK user -> default::User;
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK playlists -> default::Playlist;
  };
};
