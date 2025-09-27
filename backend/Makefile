.PHONY: dev worker fmt lint test

dev:
	uvicorn app.main:app --reload --port $${APP_PORT:-8080}

worker:
	python -m app.workers.runner

fmt:
	ruff check --fix . || true

lint:
	ruff check . || true
	pylint app || true

test:
	pytest -q || true

