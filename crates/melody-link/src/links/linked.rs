use melody_config::config::context::Context;

use crate::url::{Error, Url, parse};

pub trait Linked {
    type Str: AsRef<str>;

    fn str(&self, context: &Context<'_>) -> Self::Str;

    fn apple_music_str(&self) -> Option<Self::Str> {
        None
    }

    fn spotify_str(&self) -> Option<Self::Str> {
        None
    }

    fn yandex_music_str(&self) -> Option<Self::Str> {
        None
    }

    fn url(&self, context: &Context<'_>) -> Result<Url, Error> {
        parse(self.str(context))
    }

    fn apple_music_url(&self) -> Result<Option<Url>, Error> {
        self.apple_music_str().map(parse).transpose()
    }

    fn spotify_url(&self) -> Result<Option<Url>, Error> {
        self.spotify_str().map(parse).transpose()
    }

    fn yandex_music_url(&self) -> Result<Option<Url>, Error> {
        self.yandex_music_str().map(parse).transpose()
    }
}
