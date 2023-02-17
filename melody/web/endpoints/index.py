from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.responses import HTMLResponse

from melody.kit.core import app, database
from melody.web.core import environment
from melody.web.dependencies import optional_cookie_token_dependency

__all__ = ("get_index",)

INDEX_TEMPLATE = environment.get_template("index.html")
APP_TEMPLATE = environment.get_template("app.html")

COUNT = "{:,}"
count = COUNT.format


@app.get("/")
async def get_index(
    user_id: Optional[UUID] = Depends(optional_cookie_token_dependency)
) -> HTMLResponse:
    if user_id is None:
        statistics = await database.query_statistics()

        return HTMLResponse(
            await INDEX_TEMPLATE.render_async(
                track_count=count(statistics.track_count),
                artist_count=count(statistics.artist_count),
                album_count=count(statistics.album_count),
                playlist_count=count(statistics.playlist_count),
                user_count=count(statistics.user_count),
                stream_count=count(statistics.stream_count),
            )
        )

    return HTMLResponse(await APP_TEMPLATE.render_async())
