CREATE MIGRATION m12zxv7vq5rn3hgxtxobd6tmtlm6tdad2lzdl2vkft6uygql72qzgq
    ONTO m1qcjxgeurqtvlyr25m7sgzmpfm2rlysb5quannimqqu4xhvockdlq
{
  ALTER TYPE default::User {
      CREATE MULTI LINK albums -> default::Album;
      CREATE MULTI LINK playlists -> default::Playlist;
      CREATE MULTI LINK tracks -> default::Track;
  };
};
