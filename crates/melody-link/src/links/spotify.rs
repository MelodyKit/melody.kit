use std::fmt::Display;

pub fn artist<I: Display>(id: I) -> String {
    format!("https://open.spotify.com/artist/{id}")
}

pub fn album<I: Display>(id: I) -> String {
    format!("https://open.spotify.com/album/{id}")
}

pub fn track<I: Display>(id: I) -> String {
    format!("https://open.spotify.com/track/{id}")
}

pub fn playlist<I: Display>(id: I) -> String {
    format!("https://open.spotify.com/playlist/{id}")
}

pub fn user<I: Display>(id: I) -> String {
    format!("https://open.spotify.com/user/{id}")
}
