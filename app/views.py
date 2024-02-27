from datetime import datetime

from aiohttp import web
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic import model_validator

from app.db import get_orders_stat


class StatRequest(BaseModel):
    started_at: datetime
    finished_at: datetime

    @model_validator(mode="after")
    def check_datetime(self) -> "StatRequest":
        if self.started_at > self.finished_at:
            raise ValueError("finished_at must be greater than started_at")
        return self


async def orders_stat(request: web.Request) -> web.Response:
    try:
        if request.method == "GET":
            request_data = StatRequest(**request.rel_url.query)
        else:
            data = await request.json()
            request_data = StatRequest(**data)
    except ValidationError as e:
        return web.Response(text=e.json(), content_type="application/json", status=400)

    result = await get_orders_stat(
        request.app["db"], request_data.started_at, request_data.finished_at
    )

    return web.json_response([r.dict() for r in result])
