pub use chrono::{Datelike, NaiveDate as Date, Utc};

pub const CREATED: Date = Date::from_ymd_opt(2022, 5, 24).unwrap();

pub const fn created() -> Date {
    CREATED
}

pub fn today() -> Date {
    Utc::now().date_naive()
}
