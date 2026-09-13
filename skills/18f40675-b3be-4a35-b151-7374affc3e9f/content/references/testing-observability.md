# Testing & Observability in Enterprise Python

## 1. Pytest + Testcontainers Integration Testing

```python
import pytest
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture
async def db_session(postgres_container: PostgresContainer) -> AsyncIterator[AsyncSession]:
    # Create async connection URL from testcontainer
    db_url = postgres_container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(db_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()
```

---

## 2. Structured JSON Logging with `structlog`

```python
import logging
import structlog

def setup_logging(log_level: str = "INFO") -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(log_level)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

# Usage with context
logger.info("order_created", order_id="ord_123", amount=150.00, customer_id="cust_456")
```

---

## 3. OpenTelemetry Tracing Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

def setup_tracing(service_name: str) -> None:
    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my_service")

# Tracing a critical transaction span
async def process_transaction(tx_id: str) -> None:
    with tracer.start_as_current_span("process_transaction") as span:
        span.set_attribute("transaction.id", tx_id)
        # Business logic here
```
