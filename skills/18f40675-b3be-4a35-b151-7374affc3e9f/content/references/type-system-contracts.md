# Python Type System & Interface Contracts

## 1. Modern Type Annotations (Python 3.12+)

```python
from collections.abc import Sequence, Mapping
from typing import Any

# Use PEP 695 type parameter syntax (Python 3.12+)
def first_item[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None

# Generic class with modern syntax
class Repository[TEntity, TId]:
    def __init__(self) -> None:
        self._store: dict[TId, TEntity] = {}

    def get(self, entity_id: TId) -> TEntity | None:
        return self._store.get(entity_id)

    def save(self, entity_id: TId, entity: TEntity) -> None:
        self._store[entity_id] = entity
```

---

## 2. Protocols for Structural Subtyping (Duck Typing with Type Safety)

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Cacheable(Protocol):
    @property
    def cache_key(self) -> str:
        ...

    def to_json(self) -> str:
        ...

def store_in_cache(obj: Cacheable) -> None:
    print(f"Storing key: {obj.cache_key}, data: {obj.to_json()}")
```

---

## 3. Pydantic v2 Contract Design

```python
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class ImmutableContract(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,
    )

class UserProfileDTO(ImmutableContract):
    id: UUID
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    created_at: datetime
```
