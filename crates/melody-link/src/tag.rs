use std::{borrow::Cow, fmt, str::FromStr};

use const_macros::{const_assert, const_map_err, const_none, const_ok, const_try};
use into_static::IntoStatic;
use miette::Diagnostic;
use serde::{Deserialize, Deserializer, Serialize, Serializer, de};
use thiserror::Error;

pub const INVALID: &str = "invalid tag";

#[derive(Debug, Error, Diagnostic)]
#[error("empty tag encountered")]
#[diagnostic(code(melody::link::tag::empty), help("make sure the tag is non-empty"))]
pub struct EmptyError;

#[derive(Debug, Error, Diagnostic)]
#[error("only one byte (`{value:02x}`) encountered")]
#[diagnostic(
    code(melody::link::tag::only),
    help("make sure the tag is at least two bytes long")
)]
pub struct OnlyError {
    pub value: u8,
}

impl OnlyError {
    pub const fn new(value: u8) -> Self {
        Self { value }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum SplitErrorSource {
    Empty(#[from] EmptyError),
    Only(#[from] OnlyError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("failed to split the tag")]
#[diagnostic(
    code(melody::link::tag::split),
    help("see the report for more information")
)]
pub struct SplitError {
    #[source]
    #[diagnostic_source]
    pub source: SplitErrorSource,
}

impl SplitError {
    pub const fn new(source: SplitErrorSource) -> Self {
        Self { source }
    }

    pub const fn empty(error: EmptyError) -> Self {
        Self::new(SplitErrorSource::Empty(error))
    }

    pub const fn only(error: OnlyError) -> Self {
        Self::new(SplitErrorSource::Only(error))
    }

    pub const fn new_empty() -> Self {
        Self::empty(EmptyError)
    }

    pub const fn new_only(value: u8) -> Self {
        Self::only(OnlyError::new(value))
    }
}

pub const LIMIT: usize = 32;

const_assert!(LIMIT > 1);

pub const DOT: u8 = b'.';
pub const UNDER: u8 = b'_';

#[derive(Debug, Error, Diagnostic)]
#[error("length `{length}` exceeds the limit of `{LIMIT}`")]
#[diagnostic(
    code(melody::link::tag::limit),
    help("make sure the tag length is within the limit")
)]
pub struct LimitError {
    pub length: usize,
}

impl LimitError {
    pub const fn new(length: usize) -> Self {
        Self { length }
    }
}

pub const fn check_limit(length: usize) -> Result<(), LimitError> {
    if length > LIMIT {
        Err(LimitError::new(length))
    } else {
        Ok(())
    }
}

pub const fn is_regular(byte: u8) -> bool {
    byte.is_ascii_alphanumeric()
}

pub const fn is_special(byte: u8) -> bool {
    matches!(byte, DOT | UNDER)
}

#[derive(Debug, Error, Diagnostic)]
#[error("tags can not start with `{byte:02x}`")]
#[diagnostic(
    code(melody::link::tag::start),
    help("make sure the tag does not start with special bytes")
)]
pub struct StartError {
    pub byte: u8,
}

impl StartError {
    pub const fn new(byte: u8) -> Self {
        Self { byte }
    }
}

pub const fn check_start(byte: u8) -> Result<(), StartError> {
    if is_regular(byte) {
        Ok(())
    } else {
        Err(StartError::new(byte))
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("tags can not contain `{byte:02x}`")]
#[diagnostic(
    code(melody::link::tag::middle),
    help("make sure the tag contains only valid bytes")
)]
pub struct MiddleError {
    pub byte: u8,
}

impl MiddleError {
    pub const fn new(byte: u8) -> Self {
        Self { byte }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("bytes `{repeated:02x}` can not be consecutive")]
#[diagnostic(
    code(melody::link::tag::consecutive),
    help("see the report for more information")
)]
pub struct ConcesutiveError {
    pub repeated: u8,
}

impl ConcesutiveError {
    pub const fn new(repeated: u8) -> Self {
        Self { repeated }
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum BetweenErrorSource {
    Middle(#[from] MiddleError),
    Consecutive(#[from] ConcesutiveError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("invalid bytes between start and end")]
#[diagnostic(
    code(melody::link::tag::between),
    help("see the report for more information")
)]
pub struct BetweenError {
    #[source]
    #[diagnostic_source]
    pub source: BetweenErrorSource,
}

impl BetweenError {
    pub const fn new(source: BetweenErrorSource) -> Self {
        Self { source }
    }

    pub const fn middle(error: MiddleError) -> Self {
        Self::new(BetweenErrorSource::Middle(error))
    }

    pub const fn consecutive(error: ConcesutiveError) -> Self {
        Self::new(BetweenErrorSource::Consecutive(error))
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error("tags can not end with `{byte:02x}`")]
#[diagnostic(
    code(melody::link::tag::end),
    help("make sure the tag does not end with special bytes")
)]
pub struct EndError {
    pub byte: u8,
}

impl EndError {
    pub const fn new(byte: u8) -> Self {
        Self { byte }
    }
}

pub const fn check_end(byte: u8) -> Result<(), EndError> {
    if is_regular(byte) {
        Ok(())
    } else {
        Err(EndError::new(byte))
    }
}

#[derive(Debug, Error, Diagnostic)]
#[error(transparent)]
#[diagnostic(transparent)]
pub enum ErrorSource {
    Limit(#[from] LimitError),
    Split(#[from] SplitError),
    Start(#[from] StartError),
    End(#[from] EndError),
    Between(#[from] BetweenError),
}

#[derive(Debug, Error, Diagnostic)]
#[error("invalid tag encountered")]
#[diagnostic(code(melody::link::tag), help("make sure the tag is valid"))]
pub struct Error {
    #[source]
    #[diagnostic_source]
    pub source: ErrorSource,
}

impl Error {
    pub const fn new(source: ErrorSource) -> Self {
        Self { source }
    }

    pub const fn limit(error: LimitError) -> Self {
        Self::new(ErrorSource::Limit(error))
    }

    pub const fn split(error: SplitError) -> Self {
        Self::new(ErrorSource::Split(error))
    }

    pub const fn start(error: StartError) -> Self {
        Self::new(ErrorSource::Start(error))
    }

    pub const fn between(error: BetweenError) -> Self {
        Self::new(ErrorSource::Between(error))
    }

    pub const fn end(error: EndError) -> Self {
        Self::new(ErrorSource::End(error))
    }
}

pub const fn check_consecutive(previous: u8, byte: u8) -> Result<(), ConcesutiveError> {
    if is_special(byte) && previous == byte {
        Err(ConcesutiveError::new(byte))
    } else {
        Ok(())
    }
}

pub const fn check_middle(byte: u8) -> Result<(), MiddleError> {
    if is_regular(byte) || is_special(byte) {
        Ok(())
    } else {
        Err(MiddleError::new(byte))
    }
}

pub const fn check_between_recursive(previous: u8, bytes: &[u8]) -> Result<(), BetweenError> {
    match *bytes {
        [] => Ok(()),
        [byte, ref rest @ ..] => {
            const_try!(
                const_map_err!(check_consecutive(previous, byte) => BetweenError::consecutive)
            );

            const_try!(const_map_err!(check_middle(byte) => BetweenError::middle));

            check_between_recursive(byte, rest)
        }
    }
}

pub struct Split<'s> {
    pub start: u8,
    pub between: &'s [u8],
    pub end: u8,
}

impl<'d> Split<'d> {
    pub const fn new(start: u8, between: &'d [u8], end: u8) -> Self {
        Self {
            start,
            between,
            end,
        }
    }
}

pub const fn split(bytes: &[u8]) -> Result<Split<'_>, SplitError> {
    match *bytes {
        [] => Err(SplitError::new_empty()),
        [value] => Err(SplitError::new_only(value)),
        [start, ref between @ .., end] => Ok(Split::new(start, between, end)),
    }
}

pub const fn check_recursive(bytes: &[u8]) -> Result<(), Error> {
    const_try!(const_map_err!(check_limit(bytes.len()) => Error::limit));

    let splitted = const_try!(const_map_err!(split(bytes) => Error::split));

    const_try!(const_map_err!(check_start(splitted.start) => Error::start));

    const_try!(const_map_err!(
        check_between_recursive(splitted.start, splitted.between) => Error::between
    ));

    const_try!(const_map_err!(check_end(splitted.end) => Error::end));

    Ok(())
}

pub fn check_between_step(previous: u8, byte: u8) -> Result<u8, BetweenError> {
    check_consecutive(previous, byte).map_err(BetweenError::consecutive)?;
    check_middle(byte).map_err(BetweenError::middle)?;

    Ok(byte)
}

pub fn check_between_iterative(start: u8, between: &[u8]) -> Result<(), BetweenError> {
    between
        .iter()
        .copied()
        .try_fold(start, check_between_step)?;

    Ok(())
}

pub fn check_iterative(bytes: &[u8]) -> Result<(), Error> {
    check_limit(bytes.len()).map_err(Error::limit)?;

    let splitted = split(bytes).map_err(Error::split)?;

    check_start(splitted.start).map_err(Error::start)?;

    check_between_iterative(splitted.start, splitted.between).map_err(Error::between)?;

    check_end(splitted.end).map_err(Error::end)?;

    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Tag<'t> {
    value: Cow<'t, str>,
}

impl fmt::Display for Tag<'_> {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.value.fmt(formatter)
    }
}

impl Serialize for Tag<'_> {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        self.value.serialize(serializer)
    }
}

impl<'de> Deserialize<'de> for Tag<'_> {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let value = Cow::deserialize(deserializer)?;

        Self::new(value).map_err(de::Error::custom)
    }
}

pub type StaticTag = Tag<'static>;

impl IntoStatic for Tag<'_> {
    type Static = StaticTag;

    fn into_static(self) -> Self::Static {
        unsafe { Self::Static::new_unchecked(self.value.into_static()) }
    }
}

impl FromStr for Tag<'_> {
    type Err = Error;

    fn from_str(string: &str) -> Result<Self, Self::Err> {
        Self::check(string)?;

        Ok(unsafe { Self::owned_unchecked(string.to_owned()) })
    }
}

impl<'t> Tag<'t> {
    pub fn new(value: Cow<'t, str>) -> Result<Self, Error> {
        Self::check(value.as_ref())?;

        Ok(unsafe { Self::new_unchecked(value) })
    }

    pub const fn const_check(string: &str) -> Result<(), Error> {
        check_recursive(string.as_bytes())
    }

    pub fn check<S: AsRef<str>>(string: S) -> Result<(), Error> {
        check_iterative(string.as_ref().as_bytes())
    }

    pub fn borrowed(string: &'t str) -> Result<Self, Error> {
        Self::new(Cow::Borrowed(string))
    }

    pub fn owned(string: String) -> Result<Self, Error> {
        Self::new(Cow::Owned(string))
    }

    pub const fn const_borrowed(string: &'t str) -> Result<Self, Error> {
        const_try!(Self::const_check(string));

        Ok(unsafe { Self::borrowed_unchecked(string) })
    }

    pub const fn const_borrowed_ok(string: &'t str) -> Option<Self> {
        const_none!(const_ok!(Self::const_check(string)));

        Some(unsafe { Self::borrowed_unchecked(string) })
    }

    pub const unsafe fn new_unchecked(value: Cow<'t, str>) -> Self {
        Self { value }
    }

    pub const unsafe fn borrowed_unchecked(value: &'t str) -> Self {
        unsafe { Self::new_unchecked(Cow::Borrowed(value)) }
    }

    pub const unsafe fn owned_unchecked(value: String) -> Self {
        unsafe { Self::new_unchecked(Cow::Owned(value)) }
    }

    pub fn take(self) -> Cow<'t, str> {
        self.value
    }
}

impl Tag<'_> {
    pub fn get(&self) -> &str {
        self.value.as_ref()
    }
}

#[macro_export]
macro_rules! const_borrowed_tag {
    ($string: expr) => {
        $crate::tag::Tag::const_borrowed_ok($string).expect($crate::tag::INVALID)
    };
}
