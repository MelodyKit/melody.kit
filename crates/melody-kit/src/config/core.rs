use std::{
    borrow::Cow,
    fs::read_to_string,
    path::{Path, PathBuf},
};

use bon::Builder;
use miette::Diagnostic;
use otp_std::{Digits, Period, Skew};
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::{
    config::{
        default::{
            DEFAULT_DOMAIN, DEFAULT_EMAIL_HOST, DEFAULT_EMAIL_PORT, DEFAULT_EMAIL_SUPPORT,
            DEFAULT_EXPIRES_DAYS, DEFAULT_EXPIRES_HOURS, DEFAULT_EXPIRES_MINUTES,
            DEFAULT_EXPIRES_MONTHS, DEFAULT_EXPIRES_SECONDS, DEFAULT_EXPIRES_WEEKS,
            DEFAULT_EXPIRES_YEARS, DEFAULT_HASH_MEMORY_COST, DEFAULT_HASH_PARALLELISM,
            DEFAULT_HASH_SIZE, DEFAULT_HASH_TIME_COST, DEFAULT_IMAGE_DATA_LIMIT,
            DEFAULT_IMAGE_DIRECTORY, DEFAULT_IMAGE_SIZE_LIMIT, DEFAULT_KEYRING_BOT,
            DEFAULT_KEYRING_DISCORD, DEFAULT_KEYRING_EMAIL, DEFAULT_KEYRING_SERVICE,
            DEFAULT_KEYRING_SPOTIFY, DEFAULT_KIT_HOST, DEFAULT_KIT_PORT, DEFAULT_NAME,
            DEFAULT_OPEN, DEFAULT_REDIS_HOST, DEFAULT_REDIS_PORT, DEFAULT_TOKEN_TYPE,
            DEFAULT_TOTP_DIGITS, DEFAULT_TOTP_PERIOD, DEFAULT_TOTP_SKEW, DEFAULT_WEB_HOST,
            DEFAULT_WEB_PORT,
        },
        types::{Cost, Unit},
    },
    cow,
    load::Load,
    types::Port,
};

use super::default::{
    DEFAULT_ACCESS_SIZE, DEFAULT_AUTHORIZATION_SIZE, DEFAULT_REFRESH_SIZE,
    DEFAULT_VERIFICATION_SIZE,
};

#[derive(Debug, Error, Diagnostic)]
#[error("read failed")]
#[diagnostic(
    code(melody_kit::config::read),
    help("check that the file exists and is accessible")
)]
pub struct ReadError(#[from] pub std::io::Error);

#[derive(Debug, Error, Diagnostic)]
#[error("parsing failed")]
#[diagnostic(
    code(melody_kit::config::parse),
    help("check that the configuration is correct")
)]
pub struct ParseError(#[from] pub toml::de::Error);

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Read(#[from] ReadError),
    Parse(#[from] ParseError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("loading config from `{path}` failed")]
#[diagnostic(code(melody_kit::config), help("see the report for more information"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
    pub path: PathBuf,
}

impl Error {
    pub fn new(source: ErrorSource, path: PathBuf) -> Self {
        Self { source, path }
    }

    pub fn read(error: ReadError, path: PathBuf) -> Self {
        Self::new(error.into(), path)
    }

    pub fn parse(error: ParseError, path: PathBuf) -> Self {
        Self::new(error.into(), path)
    }

    pub fn new_read(error: std::io::Error, path: PathBuf) -> Self {
        Self::read(ReadError(error), path)
    }

    pub fn new_parse(error: toml::de::Error, path: PathBuf) -> Self {
        Self::parse(ParseError(error), path)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Keyring<'k> {
    pub service: Cow<'k, str>,
    pub email: Cow<'k, str>,
    pub bot: Cow<'k, str>,
    pub discord: Cow<'k, str>,
    pub spotify: Cow<'k, str>,
}

impl Keyring<'_> {
    pub fn into_owned(self) -> Keyring<'static> {
        Keyring {
            service: cow::into_owned(self.service),
            email: cow::into_owned(self.email),
            bot: cow::into_owned(self.bot),
            discord: cow::into_owned(self.discord),
            spotify: cow::into_owned(self.spotify),
        }
    }
}

impl Default for Keyring<'_> {
    fn default() -> Self {
        let service = Cow::Borrowed(DEFAULT_KEYRING_SERVICE);
        let email = Cow::Borrowed(DEFAULT_KEYRING_EMAIL);
        let bot = Cow::Borrowed(DEFAULT_KEYRING_BOT);
        let discord = Cow::Borrowed(DEFAULT_KEYRING_DISCORD);
        let spotify = Cow::Borrowed(DEFAULT_KEYRING_SPOTIFY);

        Self {
            service,
            email,
            bot,
            discord,
            spotify,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Email<'e> {
    pub host: Cow<'e, str>,
    pub port: Port,
    pub support: Cow<'e, str>,
}

impl Email<'_> {
    pub fn into_owned(self) -> Email<'static> {
        Email {
            host: cow::into_owned(self.host),
            port: self.port,
            support: cow::into_owned(self.support),
        }
    }
}

impl Default for Email<'_> {
    fn default() -> Self {
        let host = Cow::Borrowed(DEFAULT_EMAIL_HOST);
        let port = DEFAULT_EMAIL_PORT;
        let support = Cow::Borrowed(DEFAULT_EMAIL_SUPPORT);

        Self {
            host,
            port,
            support,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Hash {
    pub time_cost: Cost,
    pub memory_cost: Cost,
    pub parallelism: Cost,
    pub size: usize,
}

impl Default for Hash {
    fn default() -> Self {
        let time_cost = DEFAULT_HASH_TIME_COST;
        let memory_cost = DEFAULT_HASH_MEMORY_COST;
        let parallelism = DEFAULT_HASH_PARALLELISM;
        let size = DEFAULT_HASH_SIZE;

        Self {
            time_cost,
            memory_cost,
            parallelism,
            size,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Kit<'k> {
    pub host: Cow<'k, str>,
    pub port: Port,
}

impl Kit<'_> {
    pub fn into_owned(self) -> Kit<'static> {
        Kit {
            host: cow::into_owned(self.host),
            port: self.port,
        }
    }
}

impl Default for Kit<'_> {
    fn default() -> Self {
        let host = Cow::Borrowed(DEFAULT_KIT_HOST);
        let port = DEFAULT_KIT_PORT;

        Self { host, port }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Image<'i> {
    pub directory: Cow<'i, str>,
    pub data_limit: usize,
    pub size_limit: usize,
}

impl Image<'_> {
    pub fn into_owned(self) -> Image<'static> {
        Image {
            directory: cow::into_owned(self.directory),
            data_limit: self.data_limit,
            size_limit: self.size_limit,
        }
    }
}

impl Default for Image<'_> {
    fn default() -> Self {
        let directory = Cow::Borrowed(DEFAULT_IMAGE_DIRECTORY);
        let data_limit = DEFAULT_IMAGE_DATA_LIMIT;
        let size_limit = DEFAULT_IMAGE_SIZE_LIMIT;

        Self {
            directory,
            data_limit,
            size_limit,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Redis<'r> {
    pub host: Cow<'r, str>,
    pub port: Port,
}

impl Redis<'_> {
    pub fn into_owned(self) -> Redis<'static> {
        Redis {
            host: cow::into_owned(self.host),
            port: self.port,
        }
    }
}

impl Default for Redis<'_> {
    fn default() -> Self {
        let host = Cow::Borrowed(DEFAULT_REDIS_HOST);
        let port = DEFAULT_REDIS_PORT;

        Self { host, port }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Totp {
    pub digits: Digits,
    pub skew: Skew,
    pub period: Period,
}

impl Default for Totp {
    fn default() -> Self {
        let digits = DEFAULT_TOTP_DIGITS;
        let skew = DEFAULT_TOTP_SKEW;
        let period = DEFAULT_TOTP_PERIOD;

        Self {
            digits,
            skew,
            period,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Expires {
    pub years: Unit,
    pub months: Unit,
    pub weeks: Unit,
    pub days: Unit,
    pub hours: Unit,
    pub minutes: Unit,
    pub seconds: Unit,
}

impl Default for Expires {
    fn default() -> Self {
        let years = DEFAULT_EXPIRES_YEARS;
        let months = DEFAULT_EXPIRES_MONTHS;
        let weeks = DEFAULT_EXPIRES_WEEKS;
        let days = DEFAULT_EXPIRES_DAYS;
        let hours = DEFAULT_EXPIRES_HOURS;
        let minutes = DEFAULT_EXPIRES_MINUTES;
        let seconds = DEFAULT_EXPIRES_SECONDS;

        Self {
            years,
            months,
            weeks,
            days,
            hours,
            minutes,
            seconds,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Web<'w> {
    pub host: Cow<'w, str>,
    pub port: Port,
}

impl Web<'_> {
    pub fn into_owned(self) -> Web<'static> {
        Web {
            host: cow::into_owned(self.host),
            port: self.port,
        }
    }
}

impl Default for Web<'_> {
    fn default() -> Self {
        let host = Cow::Borrowed(DEFAULT_WEB_HOST);
        let port = DEFAULT_WEB_PORT;

        Self { host, port }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Verification {
    pub expires: Expires,
    pub size: usize,
}

impl Default for Verification {
    fn default() -> Self {
        let expires = Expires::default();
        let size = DEFAULT_VERIFICATION_SIZE;

        Self { expires, size }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Authorization {
    pub expires: Expires,
    pub size: usize,
}

impl Default for Authorization {
    fn default() -> Self {
        let expires = Expires::default();
        let size = DEFAULT_AUTHORIZATION_SIZE;

        Self { expires, size }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Access {
    pub expires: Expires,
    pub size: usize,
}

impl Default for Access {
    fn default() -> Self {
        let expires = Expires::default();
        let size = DEFAULT_ACCESS_SIZE;

        Self { expires, size }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Refresh {
    pub expires: Expires,
    pub size: usize,
}

impl Default for Refresh {
    fn default() -> Self {
        let expires = Expires::default();
        let size = DEFAULT_REFRESH_SIZE;

        Self { expires, size }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Builder)]
#[serde(default)]
pub struct Config<'c> {
    pub name: Cow<'c, str>,
    pub domain: Cow<'c, str>,
    pub open: Cow<'c, str>,
    pub token_type: Cow<'c, str>,
    pub keyring: Keyring<'c>,
    pub email: Email<'c>,
    pub hash: Hash,
    pub kit: Kit<'c>,
    pub image: Image<'c>,
    pub redis: Redis<'c>,
    pub totp: Totp,
    pub web: Web<'c>,
    pub verification: Verification,
    pub authorization: Authorization,
    pub access: Access,
    pub refresh: Refresh,
}

impl Default for Config<'_> {
    fn default() -> Self {
        let name = Cow::Borrowed(DEFAULT_NAME);
        let domain = Cow::Borrowed(DEFAULT_DOMAIN);
        let open = Cow::Borrowed(DEFAULT_OPEN);
        let token_type = Cow::Borrowed(DEFAULT_TOKEN_TYPE);

        let keyring = Keyring::default();
        let email = Email::default();
        let hash = Hash::default();
        let kit = Kit::default();
        let image = Image::default();
        let redis = Redis::default();
        let totp = Totp::default();
        let web = Web::default();

        let verification = Verification::default();
        let authorization = Authorization::default();
        let access = Access::default();
        let refresh = Refresh::default();

        Self {
            name,
            domain,
            open,
            token_type,
            keyring,
            email,
            hash,
            kit,
            image,
            redis,
            totp,
            web,
            verification,
            authorization,
            access,
            refresh,
        }
    }
}

impl Load for Config<'_> {
    type Error = Error;

    fn load<P: AsRef<Path>>(path: P) -> Result<Self, Self::Error> {
        let path = path.as_ref();

        let string =
            read_to_string(path).map_err(|error| Self::Error::new_read(error, path.to_owned()))?;

        let config = toml::from_str(&string)
            .map_err(|error| Self::Error::new_parse(error, path.to_owned()))?;

        Ok(config)
    }
}

pub type OwnedConfig = Config<'static>;

impl Config<'_> {
    pub fn into_owned(self) -> OwnedConfig {
        OwnedConfig {
            name: cow::into_owned(self.name),
            domain: cow::into_owned(self.domain),
            open: cow::into_owned(self.open),
            token_type: cow::into_owned(self.token_type),
            keyring: self.keyring.into_owned(),
            email: self.email.into_owned(),
            hash: self.hash,
            kit: self.kit.into_owned(),
            image: self.image.into_owned(),
            redis: self.redis.into_owned(),
            totp: self.totp,
            web: self.web.into_owned(),
            verification: self.verification,
            authorization: self.authorization,
            access: self.access,
            refresh: self.refresh,
        }
    }
}
