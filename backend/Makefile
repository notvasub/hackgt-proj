.PHONY: help install dev test clean docker-up docker-down migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -e .

dev: ## Install development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	pytest

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage

docker-up: ## Start all services with Docker Compose
	docker-compose up -d

docker-down: ## Stop all services
	docker-compose down

docker-logs: ## View logs from all services
	docker-compose logs -f

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create a new migration
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

shell: ## Open a shell in the web container
	docker-compose exec web bash

db-shell: ## Open a PostgreSQL shell
	docker-compose exec db psql -U user -d claimmax_ai

start-dev: ## Start development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

start-worker: ## Start Celery worker
	celery -A app.celery_app worker --loglevel=info

start-flower: ## Start Celery Flower monitoring
	celery -A app.celery_app flower --port=5555