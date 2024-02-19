from fastapi import Depends

from melody.kit.core import database, v1
from melody.kit.enums import Tag
from melody.kit.models.statistics import StatisticsData
from melody.kit.tokens.dependencies import token_dependency

__all__ = ("get_statistics",)


@v1.get(
    "/statistics",
    tags=[Tag.STATISTICS],
    summary="Fetches overall statistics.",
    dependencies=[Depends(token_dependency)],
)
async def get_statistics() -> StatisticsData:
    statistics = await database.query_statistics()

    return statistics.into_data()
