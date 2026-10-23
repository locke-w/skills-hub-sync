# Type System Mastery

## Basic Type Annotations

```python
from typing import Any
from collections.abc import Sequence, Mapping

# Function signatures
def process_user(name: str, age: int, active: bool = True) -> dict[str, Any]:
    return {"name": name, "age": age, "active": active}

# Use | for unions (Python 3.10+)
def find_user(user_id: int | str) -> dict[str, Any] | None:
    if isinstance(user_id, int):
        return {"id": user_id}
    return None

# Collections - prefer collections.abc
def process_items(items: Sequence[str]) -> list[str]:
    """Accepts list, tuple, or any sequence."""
    return [item.upper() for item in items]

def merge_configs(base: Mapping[str, int], override: dict[str, int]) -> dict[str, int]:
    """Mapping for read-only, dict for mutable."""
    return {**base, **override}
```

## Generic Types

```python
from typing import TypeVar, Generic, Protocol
from collections.abc import Callable, Sequence

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# Generic function
def first_element(items: Sequence[T]) -> T | None:
    return items[0] if items else None

# Generic class
class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        self._data[key] = value
```

## Protocol for Structural Typing

```python
from typing import Protocol, runtime_checkable

class Drawable(Protocol):
    def draw(self) -> str:
        ...

    @property
    def color(self) -> str:
        ...

class Circle:
    def __init__(self, radius: float, color: str) -> None:
        self.radius = radius
        self._color = color

    def draw(self) -> str:
        return f"Drawing {self._color} circle"

    @property
    def color(self) -> str:
        return self._color

def render(shape: Drawable) -> str:
    return shape.draw()
```
