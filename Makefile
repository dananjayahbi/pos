# =============================================================================
# LankaCommerce Cloud - Makefile
# =============================================================================
# Usage: make [target]
# Run 'make help' to see all available commands
# =============================================================================

.DEFAULT_GOAL := help

# Project variables
COMPOSE = docker compose
COMPOSE_PROD = docker compose -f docker-compose.yml -f docker-compose.prod.yml
BACKEND_EXEC = $(COMPOSE) exec backend
FRONTEND_EXEC = $(COMPOSE) exec frontend
MANAGE = $(BACKEND_EXEC) python manage.py

# =============================================================================
# Help
# =============================================================================

## Show this help message
help:
	@echo ""
	@echo "LankaCommerce Cloud - Available Commands"
	@echo "========================================="
	@echo ""
	@grep -E '^## ' $(MAKEFILE_LIST) | sed -e 's/## //' | while read -r line; do \
		echo "  $$line"; \
	done
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Docker Commands
# =============================================================================

## Docker Commands:

up: ## Start all containers in detached mode
	$(COMPOSE) up -d

down: ## Stop all containers
	$(COMPOSE) down

build: ## Build all containers
	$(COMPOSE) build

rebuild: ## Rebuild all containers from scratch
	$(COMPOSE) build --no-cache

logs: ## View container logs (follow mode)
	$(COMPOSE) logs -f

up-build: ## Start all containers with build
	$(COMPOSE) up -d --build

logs-backend: ## View backend container logs
	$(COMPOSE) logs -f backend

logs-frontend: ## View frontend container logs
	$(COMPOSE) logs -f frontend

logs-service: ## View logs for a specific service (usage: make logs-service s=redis)
	$(COMPOSE) logs -f $(s)

restart: ## Restart all containers
	$(COMPOSE) restart

ps: ## List running containers
	$(COMPOSE) ps

status: ## Show detailed container status and health
	@echo ""
	@echo "Container Status:"
	@echo "================="
	$(COMPOSE) ps -a
	@echo ""
	@echo "Service Health:"
	@echo "==============="
	@docker inspect --format='{{.Name}}: {{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' $$(docker compose ps -q 2>/dev/null) 2>/dev/null || echo "No containers running"
	@echo ""

# =============================================================================
# Development Commands
# =============================================================================

## Development Commands:

dev: up ## Start development environment
	@echo "Development environment started!"
	@echo "Backend:  http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Flower:   http://localhost:5555"

dev-start: ## Start development environment using dev-start.sh
	@bash docker/scripts/dev-start.sh

dev-stop: ## Stop development environment using dev-stop.sh
	@bash docker/scripts/dev-stop.sh

shell: ## Open Django shell
	$(MANAGE) shell

shell-backend: ## Open bash shell in backend container
	$(BACKEND_EXEC) bash

shell-frontend: ## Open sh shell in frontend container
	$(FRONTEND_EXEC) sh

dbshell: ## Open database shell
	$(COMPOSE) exec db psql -U postgres -d lankacommerce

db-reset: ## Reset the development database
	@bash docker/scripts/db-reset.sh

manage: ## Run Django management command (usage: make manage cmd="check")
	$(MANAGE) $(cmd)

migrate: ## Run database migrations
	$(MANAGE) migrate

makemigrations: ## Create new database migrations
	$(MANAGE) makemigrations

createsuperuser: ## Create a Django superuser
	$(MANAGE) createsuperuser

collectstatic: ## Collect static files
	$(MANAGE) collectstatic --noinput

# =============================================================================
# Testing Commands
# =============================================================================

## Testing Commands:

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	$(BACKEND_EXEC) python -m pytest

test-frontend: ## Run frontend tests
	$(FRONTEND_EXEC) npm test

coverage: ## Run backend tests with coverage report
	$(BACKEND_EXEC) python -m pytest --cov --cov-report=html
	@echo "Coverage report generated in backend/htmlcov/"

# =============================================================================
# Code Quality Commands
# =============================================================================

## Code Quality Commands:

lint: lint-backend lint-frontend ## Run all linters

lint-backend: ## Run Python linters (ruff, mypy)
	$(BACKEND_EXEC) ruff check .
	$(BACKEND_EXEC) mypy .

lint-frontend: ## Run frontend linters (ESLint)
	$(FRONTEND_EXEC) npm run lint

format: ## Format all code
	$(BACKEND_EXEC) ruff format .
	$(FRONTEND_EXEC) npm run format

format-check: ## Check code formatting without changes
	$(BACKEND_EXEC) ruff format --check .

# =============================================================================
# Utility Commands
# =============================================================================

## Utility Commands:

clean: ## Clean temporary files and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned temporary files and caches."

docker-clean: ## Remove all Docker resources (containers, images, volumes)
	$(COMPOSE) down -v --rmi local --remove-orphans
	@echo "Docker resources cleaned."

docker-prune: ## Prune unused Docker resources system-wide
	docker system prune -f
	docker volume prune -f
	@echo "Docker system pruned."

seed: ## Seed the database with sample data
	$(MANAGE) loaddata fixtures/*.json
	@echo "Database seeded successfully."

backup: ## Backup the database
	@mkdir -p backups
	$(COMPOSE) exec db pg_dump -U lcc_user lcc_dev > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backup created."

restore: ## Restore the database from the latest backup
	@echo "Restoring from latest backup..."
	$(COMPOSE) exec -T db psql -U lcc_user lcc_dev < $$(ls -t backups/*.sql | head -1)
	@echo "Database restored."

# =============================================================================
# Production Commands
# =============================================================================

## Production Commands:

prod-up: ## Start production containers
	$(COMPOSE_PROD) up -d

prod-down: ## Stop production containers
	$(COMPOSE_PROD) down

prod-build: ## Build production containers
	$(COMPOSE_PROD) build

prod-logs: ## View production container logs
	$(COMPOSE_PROD) logs -f

# =============================================================================
# Phony Targets
# =============================================================================

.PHONY: help up down build rebuild logs logs-backend logs-frontend logs-service restart ps status \
        dev dev-start dev-stop shell shell-backend shell-frontend dbshell db-reset manage \
        migrate makemigrations createsuperuser collectstatic \
        test test-backend test-frontend coverage \
        lint lint-backend lint-frontend format format-check \
        clean docker-clean docker-prune seed backup restore \
        prod-up prod-down prod-build prod-logs up-build
