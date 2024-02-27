from unittest.mock import patch

import pytest

from app.db import OrderStat


class TestOrdersStat:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method, url, data",
        (
            ("GET", "/?started_at=2021-01-01&finished_at=2021-01-02", None),
            ("POST", "/", {"started_at": "2021-01-01", "finished_at": "2021-01-02"}),
        ),
    )
    @patch(
        "app.views.get_orders_stat",
        return_value=[OrderStat(origin="origin", total_tickets=1, total_price=10)],
    )
    async def test_success(self, get_orders_stat_mock, method, url, data, test_client):
        if method == "GET":
            resp = await test_client.get(url)
        else:
            resp = await test_client.post(url, json=data)

        assert resp.status == 200
        assert await resp.json() == [{"origin": "origin", "total_price": 10.0, "total_tickets": 1}]

    @pytest.mark.asyncio
    async def test_validation_error(self, test_client):
        # 1 Empty get params
        resp = await test_client.get("/")

        assert resp.status == 400
        assert await resp.json() == [
            {
                "input": {},
                "loc": [
                    "started_at",
                ],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.6/v/missing",
            },
            {
                "input": {},
                "loc": [
                    "finished_at",
                ],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.6/v/missing",
            },
        ]

        # 2 Empty get params started_at > finished_at
        resp = await test_client.get("/?started_at=2021-01-02&finished_at=2021-01-01")

        assert resp.status == 400
        assert await resp.json() == [
            {
                "ctx": {
                    "error": "finished_at must be greater than started_at",
                },
                "input": {
                    "finished_at": "2021-01-01",
                    "started_at": "2021-01-02",
                },
                "loc": [],
                "msg": "Value error, finished_at must be greater than started_at",
                "type": "value_error",
                "url": "https://errors.pydantic.dev/2.6/v/value_error",
            },
        ]

        # 3 Incorrect datetime format
        resp = await test_client.get("/?started_at=2021-01-02&finished_at=2021-01-01sf")

        assert resp.status == 400
        assert await resp.json() == [
            {
                "ctx": {
                    "error": "unexpected extra characters at the end of the input",
                },
                "input": "2021-01-01sf",
                "loc": [
                    "finished_at",
                ],
                "msg": "Input should be a valid datetime or date, unexpected extra characters "
                "at the end of the input",
                "type": "datetime_from_date_parsing",
                "url": "https://errors.pydantic.dev/2.6/v/datetime_from_date_parsing",
            },
        ]
