CREATE MIGRATION m1bxcamoansgmekngdra26g4xpk574pw2pds4iailsfbv5thfxgnhq
    ONTO m1jorcsefhind3qv4kukpi7tnbb2rtdawze76x3lvwyccdxbgoxfjq
{
  ALTER TYPE default::User {
      CREATE MULTI LINK artists -> default::Artist;
  };
};
