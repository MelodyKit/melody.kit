from datetime import date as StandardDate
from datetime import datetime as StandardDateTime
from typing import Type

from pendulum import UTC, Date, DateTime, Duration, date
from pendulum import datetime as date_time
from pendulum import duration, from_timestamp, now, parse

from melody.shared.converter import CONVERTER

__all__ = (
    "utc_now",
    "utc_today",
    "utc_from_timestamp",
    "convert_standard_date",
    "convert_standard_date_time",
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
        tz=standard_date_time.tzinfo or UTC,  # type: ignore
    )


def structure_date_time_ignore_type(string: str, date_time_type: Type[DateTime]) -> DateTime:
    return parse(string)  # type: ignore


def unstructure_date_time(date_time: DateTime) -> str:
    return str(date_time)


def structure_date_ignore_type(string: str, date_type: Type[Date]) -> Date:
    return parse(string).date()  # type: ignore


def unstructure_date(date: Date) -> str:
    return str(date)


def structure_duration_ignore_type(seconds: float, duration_type: Type[Duration]) -> Duration:
    return duration(seconds=seconds)


def unstructure_duration(duration: Duration) -> float:
    return duration.total_seconds()  # type: ignore


CONVERTER.register_structure_hook(DateTime, structure_date_time_ignore_type)
CONVERTER.register_unstructure_hook(DateTime, unstructure_date_time)

CONVERTER.register_structure_hook(Date, structure_date_ignore_type)
CONVERTER.register_unstructure_hook(Date, unstructure_date)

CONVERTER.register_structure_hook(Duration, structure_duration_ignore_type)
CONVERTER.register_unstructure_hook(Duration, unstructure_duration)
