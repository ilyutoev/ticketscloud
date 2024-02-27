from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.routes import setup_routes
from app.settings import settings


async def setup_db() -> AsyncIOMotorDatabase:
    db = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port).app
    return db


async def app_init() -> web.Application:
    db = await setup_db()
    app = web.Application()
    app["db"] = db
    app["settings"] = settings
    setup_routes(app)
    return app


def main() -> None:
    app = app_init()
    web.run_app(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
