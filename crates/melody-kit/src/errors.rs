use std::fmt;

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use miette::Diagnostic;
use serde::{Deserialize, Serialize};
use strum::{AsRefStr, Display, EnumCount, EnumIs, EnumIter, EnumString, IntoStaticStr};
use thiserror::Error;
use uuid::Uuid;

#[derive(
    Debug,
    Clone,
    Copy,
    PartialEq,
    Eq,
    Hash,
    Default,
    AsRefStr,
    Display,
    EnumCount,
    EnumIs,
    EnumIter,
    EnumString,
    IntoStaticStr,
    Serialize,
    Deserialize,
)]
#[serde(rename_all = "snake_case")]
#[strum(serialize_all = "snake_case")]
#[non_exhaustive]
pub enum Code {
    // unknown
    #[default]
    Unknown,
    // albums
    AlbumNotFound,
    // artists
    ArtistNotFound,
    // tracks
    TrackNotFound,
    // playlists
    PlaylistNotFound,
    PlaylistImageNotFound,
    // users
    UserNotFound,
    UserImageNotFound,
    UserBlockSelfForbidden,
    UserFollowSelfForbidden,
    UserFollowSelfPlaylistsForbidden,
    // clients
    ClientNotFound,
    // streams
    StreamNotFound,
    // auth: access tokens
    AuthAccessTokenNotFound,
    AuthAccessTokenInvalid,
    AuthAccessTokenExpectedType,
    AuthAccessTokenExpectedUser,
    AuthAccessTokenExpectedUserBased,
    AuthAccessTokenScopesMissing,
    // auth: refresh tokens
    AuthRefreshTokenExpected,
    AuthRefreshTokenInvalid,
    // auth: client credentials
    AuthClientCredentialsExpected,
    AuthClientCredentialsInvalid,
    AuthClientCredentialsMismatch,
    AuthClientCredentialsNotFound,
    AuthClientCredentialsSecretMismatch,
    // auth: authorization codes
    AuthAuthorizationCodeExpected,
    AuthAuthorizationCodeInvalid,
    AuthAuthorizationCodeRedirectUriExpected,
    AuthAuthorizationCodeRedirectUriMismatch,
    // auth: verification codes
    AuthVerificationCodeInvalid,
    // auth: emails
    AuthEmailInvalid,
    AuthEmailConflict,
    AuthEmailFailed,
    AuthEmailNotFound,
    AuthEmailUnverified,
    // auth: passwords
    AuthPasswordInvalid,
    AuthPasswordMismatch,
    // auth: codes
    AuthCodeExpected,
    AuthCodeMismatch,
    AuthCodeConflict,
    AuthCodeNotFound,
    // images
    ImageUnexpectedType,
    ImageExpectedSquare,
    ImageDataTooLarge,
    ImageSizeTooLarge,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Data {
    pub code: Code,
    pub message: String,
}

impl fmt::Display for Data {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{message} ({code})",
            code = self.code,
            message = self.message
        )
    }
}

impl Data {
    pub const fn new(code: Code, message: String) -> Self {
        Self { code, message }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("{data}")]
#[diagnostic(code(melody_kit::errors))]
pub struct Error {
    pub data: Data,
    pub status: StatusCode,
}

macro_rules! error {
    ($status_code: expr, $code: expr, $($token: tt)*) => {
        $crate::errors::Error::new(
            $crate::errors::Data::new($code, format!($($token)*)),
            $status_code
        )
    }
}

pub(crate) use error;

impl Error {
    pub const fn new(data: Data, status: StatusCode) -> Self {
        Self { data, status }
    }

    pub fn internal() -> Self {
        error!(
            StatusCode::INTERNAL_SERVER_ERROR,
            Code::Unknown,
            "internal error"
        )
    }

    pub fn user_not_found(user_id: Uuid) -> Self {
        error!(
            StatusCode::NOT_FOUND,
            Code::UserNotFound,
            "user with ID `{user_id}` not found",
        )
    }

    pub fn user_not_found_by_tag<S: AsRef<str>>(tag: S) -> Self {
        let tag = tag.as_ref();

        error!(
            StatusCode::NOT_FOUND,
            Code::UserNotFound,
            "user with tag `{tag}` not found",
        )
    }
}

impl IntoResponse for Error {
    fn into_response(self) -> Response {
        (self.status, Json(self.data)).into_response()
    }
}
