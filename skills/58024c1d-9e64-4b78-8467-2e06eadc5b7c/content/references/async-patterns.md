# Async Programming Patterns

## Structured Concurrency with TaskGroup

```python
import asyncio

async def fetch_item(item_id: int) -> dict[str, int]:
    await asyncio.sleep(0.1)
    return {"id": item_id, "data": item_id * 10}

async def fetch_all(ids: list[int]) -> list[dict[str, int]]:
    tasks: list[asyncio.Task[dict[str, int]]] = []
    async with asyncio.TaskGroup() as tg:
        for item_id in ids:
            tasks.append(tg.create_task(fetch_item(item_id)))
    return [task.result() for task in tasks]
```

## Async Iterators and Context Managers

```python
from collections.abc import AsyncIterator

class AsyncResource:
    async def __aenter__(self) -> "AsyncResource":
        print("Connected")
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        print("Disconnected")

async def async_generator(n: int) -> AsyncIterator[int]:
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i
```
