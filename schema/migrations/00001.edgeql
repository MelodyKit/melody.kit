CREATE MIGRATION m135a6vwvz7w7brscexjwri3u4wklmta2miq2lpu2mpy5iroypbcrq
    ONTO initial
{
  CREATE FUTURE nonrecursive_access_policies;
  CREATE ABSTRACT TYPE default::Base {
      CREATE PROPERTY apple_music_id -> std::bigint;
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE PROPERTY spotify_id -> std::str;
      CREATE PROPERTY yandex_music_id -> std::bigint;
  };
  CREATE TYPE default::Album EXTENDING default::Base {
      CREATE REQUIRED PROPERTY album_type -> std::str;
      CREATE REQUIRED PROPERTY genres -> array<std::str> {
          SET default := (<array<std::str>>[]);
      };
      CREATE REQUIRED PROPERTY label -> std::str;
      CREATE REQUIRED PROPERTY release_date -> cal::local_date;
  };
  CREATE TYPE default::Artist EXTENDING default::Base {
      CREATE REQUIRED PROPERTY genres -> array<std::str> {
          SET default := (<array<std::str>>[]);
      };
  };
  ALTER TYPE default::Album {
      CREATE REQUIRED MULTI LINK artists -> default::Artist;
  };
  ALTER TYPE default::Artist {
      CREATE MULTI LINK albums := (.<artists[IS default::Album]);
  };
  CREATE TYPE default::Track EXTENDING default::Base {
      CREATE REQUIRED MULTI LINK artists -> default::Artist;
      CREATE REQUIRED PROPERTY genres -> array<std::str> {
          SET default := (<array<std::str>>[]);
      };
  };
  ALTER TYPE default::Album {
      CREATE REQUIRED MULTI LINK tracks -> default::Track;
      CREATE PROPERTY track_count := (SELECT
          std::count(.tracks)
      );
  };
  ALTER TYPE default::Track {
      CREATE MULTI LINK albums := (.<tracks[IS default::Album]);
  };
  CREATE TYPE default::User EXTENDING default::Base {
      CREATE MULTI LINK albums -> default::Album;
      CREATE MULTI LINK artists -> default::Artist;
      CREATE MULTI LINK tracks -> default::Track;
      CREATE REQUIRED PROPERTY email -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY password -> std::str;
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
