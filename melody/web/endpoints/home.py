from fastapi.responses import HTMLResponse

from melody.kit.core import app
from melody.web.core import environment

__all__ = ("get_home",)

TEMPLATE = environment.get_template("home.html")


@app.get("/")
async def get_home() -> HTMLResponse:
    return HTMLResponse(await TEMPLATE.render_async())
