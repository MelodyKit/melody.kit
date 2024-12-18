use chrono::{DateTime, NaiveDate, Utc};

pub type Color = u32;

pub type Port = u16;

pub type Count = u64;
pub type SignedCount = i64;

pub fn count(signed: SignedCount) -> Count {
    signed.unsigned_abs()
}

pub type Date = NaiveDate;
pub type UtcDateTime = DateTime<Utc>;
