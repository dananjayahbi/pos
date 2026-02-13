# LankaCommerce Cloud — Backend

> Django-based REST API backend for the LankaCommerce Cloud POS & ERP platform.

For the overall project documentation, see the [main README](../README.md).

---

## Overview

The backend powers all server-side logic for LankaCommerce Cloud, including multi-tenant SaaS operations, ERP modules, and the web-store API. It is built with **Django 5.x** and **Django REST Framework** and uses **django-tenants** for PostgreSQL schema-based multi-tenancy.

### Technology Stack

| Technology            | Version | Purpose                  |
| --------------------- | ------- | ------------------------ |
| Python                | 3.12+   | Programming language     |
| Django                | 5.x     | Web framework            |
| Django REST Framework | 3.15+   | REST API framework       |
| PostgreSQL            | 15+     | Database                 |
| Redis                 | 7+      | Cache and message broker |
| Celery                | 5.x     | Async task queue         |
| django-tenants        | 3.x     | Multi-tenancy            |

---

## Directory Structure

```
backend/
├── apps/              # Django applications (modular business logic)
├── config/            # Django project settings & root URL configuration
├── core/              # Shared utilities, base models, mixins, helpers
├── fixtures/          # Seed data and test fixtures (JSON/YAML)
├── locale/            # Internationalization files (en, si, ta)
├── media/             # User-uploaded files (git-ignored in production)
├── requirements/      # Pip requirement files (base, dev, prod, test)
├── static/            # Static assets collected by Django
├── templates/         # Django HTML templates (email, admin, errors)
├── tests/             # Project-wide / integration tests
├── .env.example       # Environment variable template
├── manage.py          # Django management CLI entry point
├── pyproject.toml     # Python project & tool configuration
└── README.md          # This file
```

---

## Prerequisites

Make sure you have the following installed before setting up the backend:

- **Python 3.12+** — [python.org](https://www.python.org/downloads/)
- **PostgreSQL 15+** — [postgresql.org](https://www.postgresql.org/download/)
- **Redis 7+** — [redis.io](https://redis.io/download/)
- **pip** (comes with Python) or **pipx** for CLI tools

---

## Setup

### 1. Create & activate a virtual environment

```bash
cd backend
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements/development.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your local database credentials and secrets
```

### 4. Set up the database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

The API will be available at **http://localhost:8000/**.

---

## Development Commands

### Django

| Command                            | Description                  |
| ---------------------------------- | ---------------------------- |
| `python manage.py runserver`       | Start the development server |
| `python manage.py migrate`         | Apply database migrations    |
| `python manage.py makemigrations`  | Create new migrations        |
| `python manage.py createsuperuser` | Create an admin user         |
| `python manage.py shell`           | Open the Django shell        |
| `python manage.py collectstatic`   | Collect static files         |

### Testing

| Command                 | Description                    |
| ----------------------- | ------------------------------ |
| `pytest`                | Run the full test suite        |
| `pytest --cov`          | Run tests with coverage report |
| `pytest -x`             | Stop on first failure          |
| `pytest -k "test_name"` | Run a specific test            |

### Code Quality

| Command                  | Description           |
| ------------------------ | --------------------- |
| `black .`                | Format code           |
| `black --check --diff .` | Check formatting (CI) |
| `isort .`                | Sort imports          |
| `flake8`                 | Lint code             |
| `mypy .`                 | Type-check code       |

### Code Formatting (Black)

This project uses [Black](https://black.readthedocs.io/) for Python code formatting.

**Quick Commands:**

```bash
# Format all code
make format

# Check formatting (CI)
make format-check

# Format specific file
black path/to/file.py
```

**Configuration** (`pyproject.toml`):
- Line length: 88 characters
- Target: Python 3.12
- Excludes: migrations, venv, cache

**IDE Setup:**

*VS Code* — Install the Black Formatter extension (`ms-python.black-formatter`), then add to `.vscode/settings.json`:
```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "black-formatter.args": ["--config", "pyproject.toml"]
}
```

*PyCharm* — Settings → Tools → Black → Enable "On code reformat" → Set path to Black executable.

**Guidelines:**
- Run `make format` before committing
- CI will reject unformatted code
- Do not reformat Django migrations (auto-excluded)
- Pre-commit hooks will be set up separately

### Import Sorting (isort)

This project uses [isort](https://pycqa.github.io/isort/) for import sorting, configured for Black compatibility.

**Quick Commands:**

```bash
# Sort all imports
make sort-imports

# Check sorting (CI)
make sort-imports-check

# Format + sort + lint fix in one command
make lint-fix
```

**Configuration** (`pyproject.toml`):
- Profile: black (compatible with Black formatting)
- Sections: FUTURE → STDLIB → DJANGO → THIRDPARTY → FIRSTPARTY → LOCALFOLDER
- First party: apps, config, core, utils
- Skips: migrations, venv, cache directories

### Linting (flake8 & Ruff)

We use two complementary linters:
- **flake8**: Traditional linter with plugins (bugbear, comprehensions, simplify)
- **Ruff**: Fast, modern Rust-based linter (preferred for auto-fixing)

**Quick Commands:**

```bash
# Run all linters
make lint

# Auto-fix issues with Ruff
make ruff-fix

# Full lint, format, and sort
make lint-fix

# Show flake8 statistics
make lint-stats
```

**Configuration:**
- `.flake8`: flake8 configuration (max-line-length 88, max-complexity 10)
- `pyproject.toml` → `[tool.ruff]`: Ruff configuration (F, E, W, I, B, C4, UP, SIM, PL rules)

**Ignored Rules:** E501 (line length — Black handles this), E203 (Black whitespace style)

---

## Architecture

### Multi-Tenancy

LankaCommerce Cloud uses **PostgreSQL schema-based multi-tenancy** via django-tenants. Each tenant (business/store) operates in an isolated database schema while sharing the same application instance.

### App Organization

Django apps are organized by business domain inside `apps/`:

- Each app is self-contained with its own models, views, serializers, and tests.
- Shared logic lives in `core/`.

### API Design

- RESTful endpoints powered by Django REST Framework.
- Versioned API routes (e.g., `/api/v1/`).
- JWT-based authentication.
- Standardized response format and error handling.

---

## Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov --cov-report=html

# Specific app
pytest apps/products/
```

### Writing Tests

- Place tests in the `tests/` directory of each app, or in the top-level `tests/` folder for integration tests.
- Name test files `test_*.py` and test classes `Test*`.
- Target a minimum of **80 %** code coverage.

---

## API Documentation

When the development server is running, interactive API docs are available at:

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](../LICENSE) file for details.
