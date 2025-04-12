use std::path::{Path, PathBuf};

use expand_tilde::{Error, expand_tilde_owned};

pub const DEFAULT: &str = "~/.config/melody/kit.toml";

pub fn default() -> Result<PathBuf, Error> {
    expand_tilde_owned(DEFAULT)
}

pub fn or_default<P: AsRef<Path>>(option: Option<P>) -> Result<PathBuf, Error> {
    option.map_or_else(default, expand_tilde_owned)
}
