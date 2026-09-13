# Python Modern Packaging & Tooling (pyproject.toml, uv, ruff, mypy)

## 1. Modern `pyproject.toml` (PEP 621)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "enterprise-service"
version = "0.1.0"
description = "Enterprise Python Service Architecture"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Architect Team", email = "architect@example.com" }]
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.28.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.2.0",
    "sqlalchemy[asyncio]>=2.0.28",
    "asyncpg>=0.29.0",
    "alembic>=1.13.1",
    "redis[hiredis]>=5.0.3",
    "structlog>=24.1.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.1.0",
    "pytest-asyncio>=0.23.5",
    "pytest-cov>=4.1.0",
    "testcontainers[postgres]>=3.7.1",
    "mypy>=1.9.0",
    "ruff>=0.3.3",
]

# Ruff configuration
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
    "PTH", # flake8-use-pathlib
    "RUF", # Ruff-specific rules
]
ignore = ["E501"] # Line length managed by formatter

[tool.ruff.lint.isort]
known-first-party = ["domain", "application", "infrastructure", "presentation", "config"]

# Mypy strict configuration
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true

# Pytest configuration
[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --cov=src --cov-report=term-missing --cov-fail-under=85"
testpaths = ["tests"]
asyncio_mode = "auto"
```
