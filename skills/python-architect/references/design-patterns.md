# Python Design Patterns in Enterprise Architecture

## 1. Strategy Pattern

Encapsulate algorithms and swap implementations at runtime.

```python
from typing import Protocol
from dataclasses import dataclass

class PaymentStrategy(Protocol):
    async def process_payment(self, amount: float, currency: str) -> str:
        ...

class StripePaymentStrategy:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def process_payment(self, amount: float, currency: str) -> str:
        # Stripe specific API call
        return f"stripe_tx_{amount}_{currency}"

class AlipayPaymentStrategy:
    def __init__(self, app_id: str) -> None:
        self.app_id = app_id

    async def process_payment(self, amount: float, currency: str) -> str:
        # Alipay specific API call
        return f"alipay_tx_{amount}_{currency}"

class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    async def checkout(self, amount: float, currency: str) -> str:
        return await self._strategy.process_payment(amount, currency)
```

---

## 2. Factory / Registry Pattern

Decouple object construction and dynamic resolution.

```python
from typing import Callable, ClassVar

class NotificationHandler(Protocol):
    async def send(self, recipient: str, message: str) -> None:
        ...

class NotificationRegistry:
    _registry: ClassVar[dict[str, type[NotificationHandler]]] = {}

    @classmethod
    def register(cls, channel_type: str) -> Callable[[type[NotificationHandler]], type[NotificationHandler]]:
        def decorator(handler_cls: type[NotificationHandler]) -> type[NotificationHandler]:
            cls._registry[channel_type] = handler_cls
            return handler_cls
        return decorator

    @classmethod
    def create(cls, channel_type: str, **kwargs: object) -> NotificationHandler:
        handler_cls = cls._registry.get(channel_type)
        if not handler_cls:
            raise ValueError(f"Unknown notification channel: {channel_type}")
        return handler_cls(**kwargs)

# Registration example:
@NotificationRegistry.register("email")
class EmailNotificationHandler:
    def __init__(self, smtp_host: str = "smtp.example.com") -> None:
        self.smtp_host = smtp_host

    async def send(self, recipient: str, message: str) -> None:
        print(f"Sending email to {recipient}: {message}")
```

---

## 3. Chain of Responsibility Pattern

Process requests through a pipeline of handlers.

```python
from typing import Protocol

class AuthenticationRequest:
    def __init__(self, token: str | None, api_key: str | None, session_id: str | None) -> None:
        self.token = token
        self.api_key = api_key
        self.session_id = session_id
        self.user_id: str | None = None

class AuthHandler(Protocol):
    def set_next(self, handler: "AuthHandler") -> "AuthHandler":
        ...

    async def handle(self, request: AuthenticationRequest) -> bool:
        ...

class BaseAuthHandler:
    def __init__(self) -> None:
        self._next_handler: AuthHandler | None = None

    def set_next(self, handler: AuthHandler) -> AuthHandler:
        self._next_handler = handler
        return handler

    async def handle(self, request: AuthenticationRequest) -> bool:
        if self._next_handler:
            return await self._next_handler.handle(request)
        return False

class BearerTokenAuthHandler(BaseAuthHandler):
    async def handle(self, request: AuthenticationRequest) -> bool:
        if request.token and request.token.startswith("Bearer "):
            request.user_id = f"user_from_token_{request.token[7:]}"
            return True
        return await super().handle(request)

class ApiKeyAuthHandler(BaseAuthHandler):
    async def handle(self, request: AuthenticationRequest) -> bool:
        if request.api_key and request.api_key.startswith("sk_"):
            request.user_id = f"user_from_key_{request.api_key}"
            return True
        return await super().handle(request)
```

---

## 4. Observer & Domain Event Publisher

Loose coupling for decoupled asynchronous side-effects.

```python
import asyncio
from dataclasses import dataclass
from typing import Callable, Coroutine, Any

@dataclass(frozen=True, slots=True)
class DomainEvent:
    event_name: str
    payload: dict[str, Any]

EventHandler = Callable[[DomainEvent], Coroutine[Any, Any, None]]

class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._subscribers.get(event.event_name, [])
        if not handlers:
            return
        async with asyncio.TaskGroup() as tg:
            for handler in handlers:
                tg.create_task(handler(event))
```
