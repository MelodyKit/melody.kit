use std::fmt::Display;

pub fn artist<I: Display>(id: I) -> String {
    format!("https://music.apple.com/artist/{id}")
}

pub fn album<I: Display>(id: I) -> String {
    format!("https://music.apple.com/album/{id}")
}

pub fn track<A: Display, I: Display>(album_id: A, id: I) -> String {
    format!("https://music.apple.com/album/{album_id}?i={id}")
}

pub fn playlist<I: Display>(id: I) -> String {
    format!("https://music.apple.com/playlist/{id}")
}

pub fn user<I: Display>(id: I) -> String {
    format!("https://music.apple.com/profile/{id}")
}
