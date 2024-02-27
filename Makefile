infra:
	docker-compose up -d mongo

lint:
	poetry run ruff format .
	poetry run ruff check . --fix
	poetry run mypy . --config-file pyproject.toml
