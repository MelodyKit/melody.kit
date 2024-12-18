use std::fs::{create_dir_all, write};

use expand_tilde::ExpandTilde;
use miette::Diagnostic;
use otp_std::{Digits, Period, Skew};
use thiserror::Error;

use crate::{
    config::types::{Cost, Unit},
    types::Port,
};

pub const DEFAULT_PATH: &str = "~/.config/melody/kit.toml";

pub const DEFAULT_NAME: &str = "MelodyKit";
pub const DEFAULT_DOMAIN: &str = "melodykit.app";
pub const DEFAULT_OPEN: &str = "open";
pub const DEFAULT_TOKEN_TYPE: &str = "Bearer";

pub const DEFAULT_KEYRING_SERVICE: &str = "melody.kit";
pub const DEFAULT_KEYRING_EMAIL: &str = "email";
pub const DEFAULT_KEYRING_BOT: &str = "bot";
pub const DEFAULT_KEYRING_DISCORD: &str = "discord";
pub const DEFAULT_KEYRING_SPOTIFY: &str = "spotify";

pub const DEFAULT_EMAIL_HOST: &str = "smtp.gmail.com";
pub const DEFAULT_EMAIL_PORT: Port = 587;
pub const DEFAULT_EMAIL_SUPPORT: &str = "support@melodykit.app";

// DEFAULT_EMAIL_VERIFICATION_SUBJECT = "{name}"
// DEFAULT_EMAIL_VERIFICATION_CONTENT = "{link}"

// DEFAULT_EMAIL_TEMPORARY_SUBJECT = "{name}"
// DEFAULT_EMAIL_TEMPORARY_CONTENT = "{link}"

pub const DEFAULT_HASH_MEMORY_COST: Cost = 65536;
pub const DEFAULT_HASH_TIME_COST: Cost = 4;
pub const DEFAULT_HASH_PARALLELISM: Cost = 4;
pub const DEFAULT_HASH_SIZE: usize = 32;

pub const DEFAULT_KIT_HOST: &str = "127.0.0.1";
pub const DEFAULT_KIT_PORT: Port = 1342;

pub const DEFAULT_IMAGE_DIRECTORY: &str = "~/.melody/kit/images";
pub const DEFAULT_IMAGE_DATA_LIMIT: usize = 16777216;
pub const DEFAULT_IMAGE_SIZE_LIMIT: usize = 4096;

pub const DEFAULT_REDIS_HOST: &str = "127.0.0.1";
pub const DEFAULT_REDIS_PORT: Port = 6379;

pub const DEFAULT_TOTP_DIGITS: Digits = Digits::DEFAULT;
pub const DEFAULT_TOTP_SKEW: Skew = Skew::DEFAULT;
pub const DEFAULT_TOTP_PERIOD: Period = Period::DEFAULT;

pub const DEFAULT_EXPIRES_YEARS: Unit = 0;
pub const DEFAULT_EXPIRES_MONTHS: Unit = 0;
pub const DEFAULT_EXPIRES_WEEKS: Unit = 0;
pub const DEFAULT_EXPIRES_DAYS: Unit = 0;
pub const DEFAULT_EXPIRES_HOURS: Unit = 0;
pub const DEFAULT_EXPIRES_MINUTES: Unit = 0;
pub const DEFAULT_EXPIRES_SECONDS: Unit = 0;

pub const DEFAULT_VERIFICATION_SIZE: usize = 32;
pub const DEFAULT_AUTHORIZATION_SIZE: usize = 32;
pub const DEFAULT_ACCESS_SIZE: usize = 32;
pub const DEFAULT_REFRESH_SIZE: usize = 32;

pub const DEFAULT_WEB_HOST: &str = "127.0.0.1";
pub const DEFAULT_WEB_PORT: Port = 4269;

#[derive(Debug, Error, Diagnostic)]
#[error("checking existence failed")]
#[diagnostic(
    code(melody_kit::config::defaults::check_existence),
    help("make sure the permissions are set correctly")
)]
pub struct CheckExistenceError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("creating directories failed")]
#[diagnostic(
    code(melody_kit::config::defaults::create_dir_all),
    help("see the report for more information")
)]
pub struct CreateDirAllError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("write failed")]
#[diagnostic(
    code(melody_kit::config::defaults::write),
    help("check that the path is accessible")
)]
pub struct WriteError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Expand(#[from] expand_tilde::Error),
    CheckExistence(#[from] CheckExistenceError),
    CreateDirAll(#[from] CreateDirAllError),
    Write(#[from] WriteError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("writing the default config failed")]
#[diagnostic(
    code(melody_kit::config::defaults),
    help("make sure the `{DEFAULT_PATH}` can be created")
)]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub fn expand(error: expand_tilde::Error) -> Self {
        Self::new(error.into())
    }

    pub fn check_existence(error: CheckExistenceError) -> Self {
        Self::new(error.into())
    }

    pub fn create_dir_all(error: CreateDirAllError) -> Self {
        Self::new(error.into())
    }

    pub fn write(error: WriteError) -> Self {
        Self::new(error.into())
    }

    pub fn new_expand() -> Self {
        Self::expand(expand_tilde::Error)
    }

    pub fn new_check_existence(error: std::io::Error) -> Self {
        Self::check_existence(CheckExistenceError(error))
    }

    pub fn new_create_dir_all(error: std::io::Error) -> Self {
        Self::create_dir_all(CreateDirAllError(error))
    }

    pub fn new_write(error: std::io::Error) -> Self {
        Self::write(WriteError(error))
    }
}

pub const DEFAULT_STRING: &str = include_str!("default.toml");

pub fn default_write() -> Result<bool, Error> {
    let default_path = DEFAULT_PATH.expand_tilde().map_err(Error::expand)?;

    if default_path
        .try_exists()
        .map_err(Error::new_check_existence)?
    {
        return Ok(false);
    }

    if let Some(default_dir) = default_path.parent() {
        create_dir_all(default_dir).map_err(Error::new_create_dir_all)?;
    };

    write(default_path, DEFAULT_STRING).map_err(Error::new_write)?;

    Ok(true)
}
