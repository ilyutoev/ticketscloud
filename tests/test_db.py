from datetime import datetime

import pytest
from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient

from app.db import OrderStat
from app.db import get_orders_stat
from app.settings import settings


@pytest.mark.asyncio
async def test_get_orders_stat():
    db = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port).test
    await db.orders.drop()
    await db.orders.insert_many(
        [
            {
                "status": "done",
                "done_at": datetime.fromisoformat("2023-04-09T04:58:02Z"),
                "tickets": 1,
                "origin": "widget",
                "total": Decimal128("1"),
            },
            {
                "status": "done",
                "done_at": datetime.fromisoformat("2023-04-10T04:58:02Z"),
                "tickets": 2,
                "origin": "widget",
                "total": Decimal128("2"),
            },
            {
                "status": "canceled",
                "done_at": datetime.fromisoformat("2023-04-10T04:58:02Z"),
                "tickets": 3,
                "origin": "widget",
                "total": Decimal128("3"),
            },
            {
                "status": "done",
                "done_at": datetime.fromisoformat("2023-04-10T04:58:02Z"),
                "tickets": 4,
                "origin": "web",
                "total": Decimal128("4"),
            },
            {
                "status": "done",
                "done_at": datetime.fromisoformat("2023-04-11T04:58:02Z"),
                "tickets": 5,
                "origin": "widget",
                "total": Decimal128("5"),
            },
        ]
    )

    result = await get_orders_stat(
        db=db, started_at=datetime(2023, 4, 9), finished_at=datetime(2023, 4, 11)
    )

    assert result == [
        OrderStat(origin="widget", total_tickets=3, total_price=3.0),
        OrderStat(origin="web", total_tickets=4, total_price=4.0),
    ]

    await db.orders.drop()
