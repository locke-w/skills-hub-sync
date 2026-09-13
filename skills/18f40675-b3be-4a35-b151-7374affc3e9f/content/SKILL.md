---
name: python-architect
description: Use when designing, building, refactoring, or reviewing enterprise Python applications, microservices, async systems, or library architectures. Invoke for Clean Architecture / DDD, FastAPI / Django enterprise structure, design patterns (Repository, Unit of Work, Strategy, Factory, DI), asyncio / TaskGroup concurrency, strict type contracts (Pydantic v2, Protocols, Generic types), SQLAlchemy 2.0 async ORM, testing with Pytest/Testcontainers, and production observability.
license: MIT
metadata:
  version: "1.1.0"
  domain: architecture
  triggers: Python architecture, Python architect, clean architecture, DDD, hexagonal architecture, FastAPI enterprise, async Python, SQLAlchemy 2.0, Pydantic v2, Python design patterns, Python microservices
  role: architect
  scope: architecture-and-implementation
  output-format: code-and-diagrams
  related-skills: api-and-interface-design, code-review-and-quality, performance-optimization, security-and-hardening
---

# Python Architect

Enterprise Python Architect specialist focused on Clean Architecture, Domain-Driven Design (DDD), modern async-first distributed systems, and enterprise Python 3.11+ / 3.12+ engineering.

## Core Workflow

1. **System & Domain Analysis**
   - Identify bounded contexts, core domain entities, aggregates, and value objects.
   - Establish module boundaries and enforce the **Single Canonical Owner** rule (every decision/state has exactly one owner).
   - Visualize architecture using Mermaid diagrams (Class diagrams, C4 context/container, sequence flows).

2. **Layered Architecture Design (Clean / Hexagonal)**
   - **Domain Layer**: Pure business logic, Domain Models, Value Objects, Domain Exceptions, Port/Repository Interfaces (Protocols/ABCs). Zero external framework dependencies.
   - **Application / Service Layer**: Use cases, Application Services, Command/Query handlers (CQRS), DTOs, Unit of Work coordination.
   - **Infrastructure Layer**: SQLAlchemy 2.0 Async Repositories, Redis cache, Message Brokers (RabbitMQ/Kafka), external API clients.
   - **Presentation / Interface Layer**: REST endpoints (FastAPI / DRF), CLI commands (Click/Typer), Event consumers.

3. **Interface & Type Contract Definition**
   - Define strict type contracts using Python 3.12+ type parameters, `typing.Protocol`, and Pydantic v2 models.
   - Ensure explicit input validation, immutable data structures (`frozen=True` dataclasses / BaseModel), and strict return types.

4. **Async & Concurrency Architecture**
   - Employ `asyncio.TaskGroup` for structured concurrency; eliminate unhandled fire-and-forget tasks.
   - Apply connection pooling, graceful lifecycle management (`lifespan`), and non-blocking I/O throughout.

5. **Security, Observability & Error Handling**
   - Implement RFC 7807 structured error responses and unified domain-to-HTTP exception mappers.
   - Configure structured JSON logging (`structlog`), OpenTelemetry tracing, and Prometheus metrics.

6. **Quality & Boundary Verification**
   - Enforce static quality gates: `ruff check`, `ruff format --check`, and `mypy --strict`.
   - Implement test pyramid: Unit tests with `pytest`, integration tests with `testcontainers-python`, reaching 85%+ coverage.

---

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Clean Architecture & DDD | `references/clean-architecture.md` | Layer structuring, DDD aggregates, domain events, repository/UoW |
| Python Design Patterns | `references/design-patterns.md` | Strategy, Factory, DI, Observer, Middleware, Plugin patterns |
| FastAPI & Async Backend | `references/fastapi-async-architecture.md` | Lifespan, Dependency Injection, SQLAlchemy 2.0 Async, Redis, Auth |
| Concurrency & Asyncio | `references/concurrency-async.md` | Structured concurrency, TaskGroups, ThreadPool/ProcessPool, Celery/Arq |
| Type System & Contracts | `references/type-system-contracts.md` | Protocols, Generics, Pydantic v2, strict typing, mypy rules |
| Testing & Observability | `references/testing-observability.md` | Pytest fixtures, Testcontainers, OpenTelemetry, structlog |
| Packaging & Tooling | `references/packaging-tooling.md` | pyproject.toml, uv / poetry, ruff, mypy, CI quality gates |

---

## Constraints & Architectural Rules

### MUST DO
- **Strict Typing**: Full type annotations on all public functions, classes, and return signatures.
- **Dependency Inversion**: High-level modules must depend on abstractions (Protocols/ABCs), not concrete implementations.
- **Async Safety**: Use non-blocking database drivers (e.g., `asyncpg`, `aiomysql`) and async HTTP clients (`httpx`).
- **Unified Error Handling**: Map domain exceptions to standardized HTTP status codes / RFC 7807 error envelopes.
- **Configuration Hygiene**: Use `pydantic-settings` to load environment variables; never hardcode configuration or secrets.
- **Resource Management**: Always use async context managers (`async with`) for sessions, connections, and locks.

### MUST NOT DO
- **No Circular Imports**: Eliminate circular dependencies via interface extraction or proper layer hierarchy.
- **No Blocking Calls in Async Loop**: Never use `time.sleep()`, `requests`, or synchronous I/O inside `async def` functions.
- **No Leakage of Infrastructure into Domain**: Domain entities must never inherit from ORM models (e.g., SQLAlchemy `Base`).
- **No Mutable Default Arguments**: Use `None` and initialize inside the function or use `field(default_factory=...)`.
- **No Bare Exceptions**: Never use `except:` or catch `Exception` without re-raising or structured logging.

---

## Architectural Template (FastAPI + Clean Architecture)

### Domain & Repository Interface (Port)

```python
# domain/models/order.py
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

class OrderStatus(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

@dataclass(frozen=True, slots=True)
class OrderItem:
    product_id: UUID
    quantity: int
    unit_price: float

@dataclass(slots=True)
class Order:
    id: UUID
    customer_id: UUID
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime | None = None

    @classmethod
    def create(cls, customer_id: UUID, items: list[OrderItem]) -> "Order":
        if not items:
            raise ValueError("Order must contain at least one item")
        return cls(id=uuid4(), customer_id=customer_id, items=items)

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot confirm order in {self.status} state")
        self.status = OrderStatus.CONFIRMED
```

```python
# domain/ports/order_repository.py
from typing import Protocol
from uuid import UUID
from domain.models.order import Order

class OrderRepository(Protocol):
    async def get_by_id(self, order_id: UUID) -> Order | None:
        ...

    async def save(self, order: Order) -> None:
        ...
```

### Application Service & Unit of Work

```python
# application/services/order_service.py
from dataclasses import dataclass
from uuid import UUID
from domain.models.order import Order, OrderItem
from domain.ports.order_repository import OrderRepository

@dataclass(frozen=True, slots=True)
class CreateOrderCommand:
    customer_id: UUID
    items: list[tuple[UUID, int, float]]

class OrderApplicationService:
    def __init__(self, order_repo: OrderRepository) -> None:
        self._order_repo = order_repo

    async def handle_create_order(self, cmd: CreateOrderCommand) -> UUID:
        items = [
            OrderItem(product_id=p_id, quantity=qty, unit_price=price)
            for p_id, qty, price in cmd.items
        ]
        order = Order.create(customer_id=cmd.customer_id, items=items)
        await self._order_repo.save(order)
        return order.id
```

### Presentation Layer (FastAPI REST Endpoint)

```python
# presentation/api/v1/orders.py
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from application.services.order_service import CreateOrderCommand, OrderApplicationService
from presentation.dependencies import get_order_service

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

class OrderItemSchema(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")
    unit_price: float = Field(gt=0, description="Unit price must be positive")

class CreateOrderRequest(BaseModel):
    customer_id: UUID
    items: list[OrderItemSchema] = Field(min_length=1)

class CreateOrderResponse(BaseModel):
    order_id: UUID

@router.post(
    "",
    response_model=CreateOrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
async def create_order(
    request: CreateOrderRequest,
    service: Annotated[OrderApplicationService, Depends(get_order_service)],
) -> CreateOrderResponse:
    try:
        command = CreateOrderCommand(
            customer_id=request.customer_id,
            items=[(i.product_id, i.quantity, i.unit_price) for i in request.items],
        )
        order_id = await service.handle_create_order(command)
        return CreateOrderResponse(order_id=order_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err
```

---

## Knowledge Reference

Clean Architecture, Domain-Driven Design (DDD), CQRS, Event Sourcing, FastAPI, SQLAlchemy 2.0 Async, Alembic, Pydantic v2, asyncio, uvloop, Celery, Arq, Redis, PostgreSQL / AsyncPG, RabbitMQ / Kafka, Docker, Testcontainers, Pytest, structlog, OpenTelemetry, Ruff, Mypy strict.
