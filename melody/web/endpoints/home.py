from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.responses import HTMLResponse

from melody.kit.core import app, database
from melody.web.core import environment
from melody.web.dependencies import optional_cookie_token_dependency

__all__ = ("get_home",)

PAGE_TEMPLATE = environment.get_template("page.html")
HOME_TEMPLATE = environment.get_template("home.html")

FORMAT = "{:,}"
format = FORMAT.format


@app.get("/")
async def get_home(
    user_id: Optional[UUID] = Depends(optional_cookie_token_dependency)
) -> HTMLResponse:
    if user_id is None:
        statistics = await database.query_statistics()

        return HTMLResponse(
            await PAGE_TEMPLATE.render_async(
                track_count=format(statistics.track_count),
                artist_count=format(statistics.artist_count),
                album_count=format(statistics.album_count),
                playlist_count=format(statistics.playlist_count),
                user_count=format(statistics.user_count),
                premium_user_count=format(statistics.premium_user_count),
            )
        )

    return HTMLResponse(await HOME_TEMPLATE.render_async())
