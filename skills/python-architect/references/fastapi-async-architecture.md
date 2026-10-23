# Enterprise FastAPI & Async Architecture

## 1. Application Lifespan & Dependency Wiring

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.database.session import init_db_engine, close_db_engine
from infrastructure.cache.redis_client import init_redis, close_redis

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: Initialize connections, thread pools, warm-up caches
    db_engine = await init_db_engine()
    redis_client = await init_redis()
    app.state.db_engine = db_engine
    app.state.redis = redis_client
    yield
    # Shutdown: Graceful drain and cleanup
    await close_redis(redis_client)
    await close_db_engine(db_engine)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Enterprise Microservice",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    # Register routers and middlewares
    return app
```

---

## 2. SQLAlchemy 2.0 Async Session Management

```python
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

class DatabaseSessionManager:
    def __init__(self, db_url: str) -> None:
        self.engine: AsyncEngine = create_async_engine(
            db_url,
            echo=False,
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600,
            pool_pre_ping=True,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        await self.engine.dispose()

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
```

---

## 3. Dependency Injection in FastAPI

```python
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from domain.ports.user_repository import UserRepository
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from application.services.user_service import UserApplicationService

async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_manager = request.app.state.db_session_manager
    async for session in session_manager.get_session():
        yield session

def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserRepository:
    return SQLAlchemyUserRepository(session)

def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserApplicationService:
    return UserApplicationService(user_repo=user_repo)
```

---

## 4. RFC 7807 Global Exception Handling

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

class ProblemDetail(BaseModel):
    type: str = Field(default="about:blank")
    title: str
    status: int
    detail: str
    instance: str | None = None

class DomainException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class EntityNotFoundException(DomainException):
    pass

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundException) -> JSONResponse:
        problem = ProblemDetail(
            title="Resource Not Found",
            status=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
            instance=str(request.url),
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=problem.model_dump(),
            media_type="application/problem+json",
        )
```
