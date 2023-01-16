from datetime import date as StandardDate
from datetime import datetime as StandardDateTime

from pendulum import UTC, Date, DateTime, date
from pendulum import datetime as date_time
from pendulum import now

__all__ = ("convert_standard_date", "convert_standard_date_time", "utc_now", "utc_today")


def utc_now() -> DateTime:
    return now(UTC)


def utc_today() -> Date:
    return utc_now().date()  # type: ignore


def convert_standard_date(standard_date: StandardDate) -> Date:
    return date(standard_date.year, standard_date.month, standard_date.day)


def convert_standard_date_time(standard_date_time: StandardDateTime) -> DateTime:
    return date_time(
        standard_date_time.year,
        standard_date_time.month,
        standard_date_time.day,
        standard_date_time.hour,
        standard_date_time.minute,
        standard_date_time.second,
        standard_date_time.microsecond,
        standard_date_time.tzinfo,  # type: ignore
    )
