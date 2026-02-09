from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass(frozen=True, slots=True)
class Opinion:
    perspective_id: str
    proposal: Mapping[str, Any]
    confidence: float
    rationale: str


Perspective = Callable[[Mapping[str, Any], int], Opinion]
