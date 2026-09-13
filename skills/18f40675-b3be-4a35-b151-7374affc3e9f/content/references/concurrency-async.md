# Python Concurrency & Async Mastery

## 1. Structured Concurrency with `asyncio.TaskGroup` (Python 3.11+)

Always prefer `asyncio.TaskGroup` over `asyncio.gather()` for structured lifecycle and automatic cancellation on failure.

```python
import asyncio
from typing import Sequence

async def fetch_user_data(user_id: str) -> dict[str, str]:
    await asyncio.sleep(0.05)
    return {"user_id": user_id, "name": "Alice"}

async def fetch_user_orders(user_id: str) -> list[str]:
    await asyncio.sleep(0.08)
    return ["order_1", "order_2"]

async def load_user_dashboard(user_id: str) -> dict[str, object]:
    user_task: asyncio.Task[dict[str, str]]
    orders_task: asyncio.Task[list[str]]

    async with asyncio.TaskGroup() as tg:
        user_task = tg.create_task(fetch_user_data(user_id))
        orders_task = tg.create_task(fetch_user_orders(user_id))

    # Reached only when all tasks in TaskGroup succeed.
    # If any task raises an exception, other tasks are cancelled and an ExceptionGroup is raised.
    return {
        "user": user_task.result(),
        "orders": orders_task.result(),
    }
```

---

## 2. Handling CPU-bound Work vs I/O-bound Work

| Workload Type | Solution | Tool / Pattern |
|---|---|---|
| Async I/O (HTTP, DB, Cache) | Event Loop | `asyncio`, `httpx`, `asyncpg` |
| Sync I/O (Legacy sync SDKs) | Thread Pool | `asyncio.to_thread(sync_func, *args)` |
| Heavy CPU (Crypto, Image/ML) | Process Pool | `concurrent.futures.ProcessPoolExecutor` |
| Distributed Background Tasks | Task Queue | `Celery` / `Arq` / `Redis Queue` |

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy_hash_calculation(data: bytes) -> str:
    # CPU bound operation
    import hashlib
    return hashlib.sha256(data).hexdigest()

async def process_payload(data: bytes, executor: ProcessPoolExecutor) -> str:
    loop = asyncio.get_running_loop()
    # Offload CPU calculation to child process without blocking the event loop
    result = await loop.run_in_executor(executor, cpu_heavy_hash_calculation, data)
    return result
```

---

## 3. Rate Limiting & Concurrency Throttling

```python
import asyncio

class ConcurrencyThrottler:
    def __init__(self, max_concurrent: int) -> None:
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def run(self, coro: object) -> object:
        async with self._semaphore:
            return await coro
```
