from datetime import date as StandardDate
from datetime import datetime as StandardDateTime

from pendulum import UTC, Date, DateTime, date
from pendulum import datetime as date_time
from pendulum import from_timestamp, now

__all__ = (
    "convert_standard_date",
    "convert_standard_date_time",
    "utc_from_timestamp",
    "utc_now",
    "utc_today",
)


def utc_now() -> DateTime:
    return now(UTC)


def utc_today() -> Date:
    return utc_now().date()  # type: ignore


def utc_from_timestamp(timestamp: float) -> DateTime:
    return from_timestamp(timestamp, UTC)


def convert_standard_date(standard_date: StandardDate) -> Date:
    return date(year=standard_date.year, month=standard_date.month, day=standard_date.day)


def convert_standard_date_time(standard_date_time: StandardDateTime) -> DateTime:
    return date_time(
        year=standard_date_time.year,
        month=standard_date_time.month,
        day=standard_date_time.day,
        hour=standard_date_time.hour,
        minute=standard_date_time.minute,
        second=standard_date_time.second,
        microsecond=standard_date_time.microsecond,
        tz=standard_date_time.tzinfo,  # type: ignore
    )
