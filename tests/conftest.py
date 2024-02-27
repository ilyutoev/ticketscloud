import pytest
from aiohttp import web

from app.routes import setup_routes


@pytest.fixture
def test_client(loop, aiohttp_client):
    app = web.Application()
    setup_routes(app)
    app["db"] = "test_db"
    return loop.run_until_complete(aiohttp_client(app))
