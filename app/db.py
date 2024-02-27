from datetime import datetime

from motor.core import AgnosticDatabase
from pydantic import BaseModel


class OrderStat(BaseModel):
    origin: str
    total_tickets: int
    total_price: float


async def get_orders_stat(
    db: AgnosticDatabase, started_at: datetime, finished_at: datetime
) -> list[OrderStat]:
    result = []
    pipeline = [
        {"$match": {"status": "done", "done_at": {"$gte": started_at, "$lt": finished_at}}},
        {
            "$group": {
                "_id": "$origin",
                "total_tickets": {"$sum": "$tickets"},
                "total_price": {"$sum": "$total"},
            }
        },
    ]

    async for doc in db.orders.aggregate(pipeline):
        result.append(
            OrderStat(
                origin=doc["_id"],
                total_tickets=doc["total_tickets"],
                total_price=float(doc["total_price"].to_decimal()),
            )
        )

    return result
