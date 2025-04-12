use std::fmt::Display;

pub const SEPARATOR: &str = ", ";

pub fn tick<D: Display>(display: D) -> String {
    format!("`{display}`")
}

pub fn bullet<D: Display>(display: D) -> String {
    format!("- {display}")
}

pub fn with_url<T: Display, U: Display>(target: T, url: U) -> String {
    format!("[{target}]({url})")
}
