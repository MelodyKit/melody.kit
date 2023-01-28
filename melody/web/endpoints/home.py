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


@app.get("/")
async def get_home(
    user_id: Optional[UUID] = Depends(optional_cookie_token_dependency)
) -> HTMLResponse:
    if user_id is None:
        statistics = await database.query_statistics()

        return HTMLResponse(
            await PAGE_TEMPLATE.render_async(
                track_count=statistics.track_count,
                artist_count=statistics.artist_count,
                album_count=statistics.album_count,
                playlist_count=statistics.playlist_count,
                user_count=statistics.user_count,
            )
        )

    return HTMLResponse(await HOME_TEMPLATE.render_async())
