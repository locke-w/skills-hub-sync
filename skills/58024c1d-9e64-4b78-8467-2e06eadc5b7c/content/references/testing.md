# Pytest Testing Patterns

## Fixtures and Mocking

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_service() -> AsyncMock:
    service = AsyncMock()
    service.get_status.return_value = "OK"
    return service

@pytest.mark.asyncio
async def test_service_status(mock_service: AsyncMock) -> None:
    status = await mock_service.get_status()
    assert status == "OK"
```
