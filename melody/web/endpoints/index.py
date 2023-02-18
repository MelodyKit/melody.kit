from fastapi.responses import HTMLResponse

from melody.kit.core import app, database
from melody.web.core import environment

__all__ = ("get_index",)

INDEX_TEMPLATE = environment.get_template("index.html")

COUNT = "{:,}"
count = COUNT.format


@app.get("/")
async def get_index() -> HTMLResponse:
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
