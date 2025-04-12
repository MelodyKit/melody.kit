use std::fmt::Display;

pub fn artist<I: Display>(id: I) -> String {
    format!("https://music.yandex.com/artist/{id}")
}

pub fn album<I: Display>(id: I) -> String {
    format!("https://music.yandex.com/album/{id}")
}

pub fn track<A: Display, I: Display>(album_id: A, id: I) -> String {
    format!("https://music.yandex.com/album/{album_id}/track/{id}")
}

pub fn playlist<U: Display, I: Display>(user_id: U, id: I) -> String {
    format!("https://music.yandex.com/users/{user_id}/playlists/{id}")
}

pub fn user<I: Display>(id: I) -> String {
    format!("https://music.yandex.com/users/{id}")
}
