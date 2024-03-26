## Ticketscloud test

### Launch app

Setup mongodb and envs (or use default):

MONGO_HOST
MONGO_PORT

```shell
> pip install "poetry==1.4.2"
> poetry install
> python main.py
```

### Dev

- `make infra` to run dev mongodb
- `mongoimport -d app -c orders --uri mongodb://localhost:27017 fake_orders.json` for load test data (into mongo container and app folder)
- `make lint` for lint and mypy
- `pytest .` for run tests 
