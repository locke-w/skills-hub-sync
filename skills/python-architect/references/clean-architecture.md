# Clean Architecture & Domain-Driven Design (DDD) in Python

## 1. Layered Architecture Principles

Clean Architecture organizes the system into concentric layers where the dependency rule strictly points inwards:

```
+-------------------------------------------------------------+
|                      Presentation Layer                     |
|  - FastAPI Routers / Controllers / REST API                 |
|  - CLI Commands (Typer/Click) / Event Subscribers           |
+-------------------------------------------------------------+
                              | (depends on)
                              v
+-------------------------------------------------------------+
|                      Application Layer                      |
|  - Use Cases / Application Services                         |
|  - Command & Query Handlers (CQRS)                          |
|  - DTOs / Input & Output Models                             |
|  - Unit of Work (UoW) Abstraction                           |
+-------------------------------------------------------------+
                              | (depends on)
                              v
+-------------------------------------------------------------+
|                        Domain Layer                         |
|  - Domain Entities & Aggregates                             |
|  - Value Objects (Immutable)                                |
|  - Domain Events & Domain Exceptions                        |
|  - Port Interfaces (Repository / Notification Protocols)    |
+-------------------------------------------------------------+
                              ^
                              | (implements interfaces / ports)
+-------------------------------------------------------------+
|                    Infrastructure Layer                     |
|  - SQLAlchemy 2.0 Async Repositories                        |
|  - Redis Cache / Message Broker Clients (Kafka / RabbitMQ)  |
|  - External HTTP / Third-party Service Adapters             |
|  - Database Migrations (Alembic)                            |
+-------------------------------------------------------------+
```

---

## 2. Directory Structure

```
src/
└── my_service/
    ├── domain/                   # Enterprise Core / Zero 3rd-party dependencies
    │   ├── exceptions.py         # Domain-specific errors
    │   ├── models/               # Aggregates, Entities, Value Objects
    │   │   ├── base.py
    │   │   └── user.py
    │   └── ports/                # Abstract interfaces (Protocols)
    │       ├── user_repository.py
    │       └── notification_service.py
    │
    ├── application/              # Orchestration & Use cases
    │   ├── dtos/                 # Data Transfer Objects
    │   ├── services/             # Application services
    │   │   └── user_service.py
    │   ├── commands/             # Write operations (CQRS)
    │   ├── queries/              # Read operations (CQRS)
    │   └── unit_of_work.py       # Transaction boundary interface
    │
    ├── infrastructure/           # Implementation of external adapters
    │   ├── database/             # SQLAlchemy setup, models, engine
    │   │   ├── models.py         # ORM mapper models
    │   │   └── session.py        # Async session factory
    │   ├── repositories/         # Concrete repository implementations
    │   │   └── user_repository.py
    │   ├── external/             # Third-party API clients
    │   └── messaging/            # Event publishers / consumers
    │
    ├── presentation/             # Entry points
    │   ├── api/                  # FastAPI endpoints
    │   │   ├── v1/
    │   │   └── deps.py           # Dependency injection providers
    │   ├── middleware/           # Logging, timing, CORS, auth
    │   └── schemas/              # Pydantic request/response schemas
    │
    └── config/                   # Configuration & Settings
        └── settings.py           # Pydantic-settings
```

---

## 3. Domain Model Implementation

```python
# domain/models/user.py
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4
from domain.exceptions import DomainValidationError

class UserRole(StrEnum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"

@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value or "." not in self.value:
            raise DomainValidationError(f"Invalid email address: {self.value}")

@dataclass(slots=True)
class User:
    id: UUID
    email: Email
    hashed_password: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, email: str, hashed_password: str, role: UserRole = UserRole.MEMBER) -> "User":
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            email=Email(email),
            hashed_password=hashed_password,
            role=role,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def deactivate(self) -> None:
        if not self.is_active:
            raise DomainValidationError("User is already deactivated")
        self.is_active = False
        self.updated_at = datetime.utcnow()
```

---

## 4. Port Interface (Repository & Unit of Work)

```python
# domain/ports/user_repository.py
from typing import Protocol
from uuid import UUID
from domain.models.user import User

class UserRepository(Protocol):
    async def get_by_id(self, user_id: UUID) -> User | None:
        ...

    async def get_by_email(self, email: str) -> User | None:
        ...

    async def save(self, user: User) -> None:
        ...

    async def delete(self, user_id: UUID) -> None:
        ...
```

```python
# application/unit_of_work.py
from typing import Protocol
from domain.ports.user_repository import UserRepository

class UnitOfWork(Protocol):
    users: UserRepository

    async def __aenter__(self) -> "UnitOfWork":
        ...

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
```

---

## 5. Infrastructure Layer (SQLAlchemy 2.0 Async Repository)

```python
# infrastructure/repositories/user_repository.py
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.user import User, Email, UserRole
from domain.ports.user_repository import UserRepository
from infrastructure.database.models import UserORM

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def save(self, user: User) -> None:
        orm = await self._session.get(UserORM, user.id)
        if not orm:
            orm = UserORM(
                id=user.id,
                email=user.email.value,
                hashed_password=user.hashed_password,
                role=user.role.value,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self._session.add(orm)
        else:
            orm.email = user.email.value
            orm.role = user.role.value
            orm.is_active = user.is_active
            orm.updated_at = user.updated_at

    def _to_domain(self, orm: UserORM) -> User:
        return User(
            id=orm.id,
            email=Email(orm.email),
            hashed_password=orm.hashed_password,
            role=UserRole(orm.role),
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
```
