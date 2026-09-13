# Modern Python Packaging with uv and pyproject.toml

## uv Package Manager

```bash
# Initialize new project
uv init --app my-service

# Add dependencies
uv add fastapi pydantic sqlalchemy asyncpg

# Add development dependencies
uv add --dev pytest ruff mypy

# Run commands within virtualenv
uv run pytest
uv run ruff check .
```
