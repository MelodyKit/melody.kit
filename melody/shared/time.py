from datetime import date as StandardDate
from datetime import datetime as StandardDateTime
from typing import Type

from pendulum import UTC, Date, DateTime, Duration, date, duration, from_timestamp, now, parse
from pendulum import datetime as date_time
from typing_aliases import is_instance

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
    return utc_now().date()


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
        tz=standard_date_time.tzinfo or UTC,
    )


def unstructure_date_time(date_time: DateTime) -> str:
    return date_time.to_iso8601_string()


NOT_DATE_TIME = "`{}` does not represent date/time"
not_date_time = NOT_DATE_TIME.format


def structure_date_time(string: str) -> DateTime:
    result = parse(string)

    if is_instance(result, DateTime):
        return result

    raise ValueError(not_date_time(string))


def structure_date_time_ignore_type(string: str, date_time_type: Type[DateTime]) -> DateTime:
    return structure_date_time(string)


def unstructure_date(date: Date) -> str:
    return date.to_date_string()


def structure_date(string: str) -> Date:
    return structure_date_time(string).date()


def structure_date_ignore_type(string: str, date_type: Type[Date]) -> Date:
    return structure_date(string)


# NOTE: since we operate on `duration_ms` directly, durations are represented as seconds
# the main usage of durations is to denote `expires_in` fields, which should be in seconds


def unstructure_duration(duration: Duration) -> int:
    return int(duration.total_seconds())


def structure_duration(seconds: int) -> Duration:
    return duration(seconds=seconds)


def structure_duration_ignore_type(seconds: int, duration_type: Type[Duration]) -> Duration:
    return structure_duration(seconds)


CONVERTER.register_structure_hook(DateTime, structure_date_time_ignore_type)
CONVERTER.register_unstructure_hook(DateTime, unstructure_date_time)

CONVERTER.register_structure_hook(Date, structure_date_ignore_type)
CONVERTER.register_unstructure_hook(Date, unstructure_date)

CONVERTER.register_structure_hook(Duration, structure_duration_ignore_type)
CONVERTER.register_unstructure_hook(Duration, unstructure_duration)
