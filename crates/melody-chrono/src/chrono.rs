use chrono::{DateTime, NaiveDate, Utc};

pub type Date = NaiveDate;

pub type UtcDateTime = DateTime<Utc>;

pub const CREATED: Date = Date::from_ymd_opt(2022, 5, 24).unwrap();

pub const fn created() -> Date {
    CREATED
}

pub fn today() -> Date {
    Utc::now().date_naive()
}
