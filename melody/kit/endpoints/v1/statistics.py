from melody.kit.core import database, v1
from melody.kit.enums import Tag
from melody.kit.models.statistics import StatisticsData

__all__ = ("get_statistics",)


@v1.get(
    "/statistics",
    tags=[Tag.STATISTICS],
    summary="Fetches overall statistics.",
)
async def get_statistics() -> StatisticsData:
    statistics = await database.query_statistics()

    return statistics.into_data()
