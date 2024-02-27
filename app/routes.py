from aiohttp import web

from app.views import orders_stat


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", orders_stat)
    app.router.add_post("/", orders_stat)
