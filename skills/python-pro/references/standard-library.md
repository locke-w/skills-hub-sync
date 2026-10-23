# Standard Library Best Practices

## Pathlib over os.path

```python
from pathlib import Path

# Safe path operations
base_dir = Path("/var/log")
target_file = base_dir / "app" / "service.log"
target_file.parent.mkdir(parents=True, exist_ok=True)

if target_file.exists():
    content = target_file.read_text(encoding="utf-8")
```

## Dataclasses with Slots and Frozen

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Coordinate:
    x: float
    y: float
    tags: tuple[str, ...] = field(default_factory=tuple)
```
