CREATE MIGRATION m12wd5zsrwkyzghtgs57il4fbu5vraprymjyaxo7acvdytthdx7z5a
    ONTO m1bxcamoansgmekngdra26g4xpk574pw2pds4iailsfbv5thfxgnhq
{
  ALTER TYPE default::Base {
      CREATE PROPERTY youtube_music_id -> std::str;
  };
};
