pub const SEPARATOR: &str = ", ";

pub fn tick<S: AsRef<str>>(string: S) -> String {
    format!("`{}`", string.as_ref())
}

pub fn bullet<S: AsRef<str>>(string: S) -> String {
    format!("- {}", string.as_ref())
}

pub fn with_url<T: AsRef<str>, U: AsRef<str>>(target: T, url: U) -> String {
    format!("[{}]({})", target.as_ref(), url.as_ref())
}
