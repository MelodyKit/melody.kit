use std::fmt;

use axum::{
    Json,
    http::StatusCode,
    response::{IntoResponse, Response},
};
use into_static::IntoStatic;
use melody_enum::melody_enum;
use melody_link::{id::Id, tag::Tag};
use miette::Diagnostic;
use non_empty_str::{CowStr, StaticCowStr, const_borrowed_str};
use serde::{Deserialize, Serialize};
use thiserror::Error;

melody_enum! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
    #[non_exhaustive]
    pub Code {
        // unknown
        #[default]
        Unknown => unknown,
        // albums
        AlbumNotFound => album::not_found,
        // artists
        ArtistNotFound => artist::not_found,
        // tracks
        TrackNotFound => track::not_found,
        // playlists
        PlaylistNotFound => playlist::not_found,
        PlaylistImageNotFound => playlist::image::not_found,
        // users
        UserNotFound => user::not_found,
        UserImageNotFound => user::image::not_found,
        SelfBlockForbidden => self::block::forbidden,
        SelfFollowForbidden => self::follow::forbidden,
        SelfPlaylistFollowForbidden => self::playlist::follow::forbidden,
        // clients
        ClientNotFound => client::not_found,
        // streams
        StreamNotFound => stream::not_found,
        // auth: access tokens
        AuthAccessTokenNotFound => auth::access_token::not_found,
        AuthAccessTokenInvalid => auth::access_token::invalid,
        AuthAccessTokenTypeExpected => auth::access_token::type::expected,
        AuthAccessTokenUserExpected => auth::access_token::expected_user,
        AuthAccessTokenUserBasedExpected => auth::access_token::user_based::expected,
        AuthAccessTokenScopeMissing => auth::access_token::scope::missing,
        // auth: refresh tokens
        AuthRefreshTokenExpected => auth::refresh_token::expected,
        AuthRefreshTokenInvalid => auth::refresh_token::invalid,
        // auth: client credentials
        AuthClientCredentialsExpected => auth::client_credentials::expected,
        AuthClientCredentialsInvalid => auth::client_credentials::invalid,
        AuthClientCredentialsMismatch => auth::client_credentials::mismatch,
        AuthClientCredentialsNotFound => auth::client_credentials::not_found,
        AuthClientCredentialsSecretMismatch => auth::client_credentials::secret::mismatch,
        // auth: authorization codes
        AuthAuthorizationCodeExpected => auth::authorization_code::expected,
        AuthAuthorizationCodeInvalid => auth::authorization_code::invalid,
        AuthAuthorizationCodeRedirectUriExpected => auth::authorization_code::redirect_uri::expected,
        AuthAuthorizationCodeRedirectUriMismatch => auth::authorization_code::redirect_uri::mismatch,
        // auth: verification codes
        AuthVerificationCodeInvalid => auth::verification_code::invalid,
        // auth: emails
        AuthEmailInvalid => auth::email::invalid,
        AuthEmailConflict => auth::email::conflict,
        AuthEmailFailed => auth::email::failed,
        AuthEmailNotFound => auth::email::not_found,
        AuthEmailUnverified => auth::email::unverified,
        // auth: passwords
        AuthPasswordInvalid => auth::password::invalid,
        AuthPasswordMismatch => auth::password::mismatch,
        // auth: codes
        AuthCodeExpected => auth::code::expected,
        AuthCodeMismatch => auth::code::mismatch,
        AuthCodeConflict => auth::code::conflict,
        AuthCodeNotFound => auth::code::not_found,
        // images
        ImageUnexpectedType => image::type::unexpected,
        ImageSquareExpected => image::square::expected,
        ImageDataTooLarge => image::data::too_large,
        ImageSizeTooLarge => image::size::too_large,
    }
}

pub type Message<'m> = CowStr<'m>;

pub type StaticMessage = StaticCowStr;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Data<'d> {
    pub code: Code,
    pub message: Message<'d>,
}

impl fmt::Display for Data<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{message} ({code})",
            code = self.code,
            message = self.message
        )
    }
}

impl<'d> Data<'d> {
    pub const fn new(code: Code, message: Message<'d>) -> Self {
        Self { code, message }
    }
}

pub const INTERNAL_ERROR: StaticMessage = const_borrowed_str!("internal error");

impl Data<'_> {
    pub const INTERNAL_ERROR: Self = Self::new(Code::Unknown, INTERNAL_ERROR);
}

pub type StaticData = Data<'static>;

impl IntoStatic for Data<'_> {
    type Static = StaticData;

    fn into_static(self) -> Self::Static {
        Self::Static::new(self.code, self.message.into_static())
    }
}

pub type Status = StatusCode;

#[derive(Debug, Error, Diagnostic)]
#[error("{data}")]
#[diagnostic(code(melody::kit::errors))]
pub struct Error {
    pub data: StaticData,
    pub status: Status,
}

pub const MESSAGE: &str = "message must be non-empty";

#[macro_export]
macro_rules! error {
    ($code: ident, $status: ident, $($token: tt)*) => {
        $crate::errors::Error::new(
            $crate::errors::StaticData::new(
                $crate::errors::Code::$code,
                $crate::errors::Message::owned(format!($($token)*)).expect($crate::errors::MESSAGE),
            ),
            $crate::errors::Status::$status,
        )
    };
}

impl Error {
    pub const fn new(data: StaticData, status: StatusCode) -> Self {
        Self { data, status }
    }

    pub fn internal<E: std::error::Error>(_error: E) -> Self {
        Self::INTERNAL
    }

    pub fn user_not_found(id: Id) -> Self {
        error!(UserNotFound, NOT_FOUND, "user with id `{id}` not found")
    }

    pub fn user_not_found_by_tag(tag: &Tag<'_>) -> Self {
        error!(UserNotFound, NOT_FOUND, "user `{tag}` not found",)
    }

    pub fn artist_not_found(id: Id) -> Self {
        error!(ArtistNotFound, NOT_FOUND, "artist with id `{id}` not found")
    }

    pub const INTERNAL: Self = Self::new(
        StaticData::INTERNAL_ERROR,
        StatusCode::INTERNAL_SERVER_ERROR,
    );
}

impl IntoResponse for Error {
    fn into_response(self) -> Response {
        (self.status, Json(self.data)).into_response()
    }
}
