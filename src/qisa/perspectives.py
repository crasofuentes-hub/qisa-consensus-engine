from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class Opinion:
    name: str
    values: Mapping[str, Any]
    confidence: float
    rationale: str = ""

    @property
    def perspective_id(self) -> str:
        """
        Stable deterministic identifier used for tie-breaking.
        We derive it from `name` to avoid requiring callers to pass extra fields.
        """
        return hashlib.sha256(self.name.encode("utf-8")).hexdigest()[:16]

    @property
    def proposal(self) -> Mapping[str, Any]:
        # Backwards-compat: older code refers to "proposal"
        return self.values

    def as_mapping(self) -> Mapping[str, Any]:
        # Stable external representation (useful for trace export / debugging)
        return {
            "name": self.name,
            "values": dict(self.values),
            "confidence": float(self.confidence),
            "rationale": self.rationale,
        }


# A Perspective is a deterministic callable: (state, step) -> Opinion
Perspective = Callable[[Mapping[str, Any], int], Opinion]


def make_default_perspectives() -> list[Perspective]:
    """
    Default deterministic perspectives for numeric target scenarios.
    They must be:
      - pure (no randomness)
      - deterministic given (state, step)
      - return Opinion(values={"x_target": <number>})
    """

    def _get_int(state: Mapping[str, Any], key: str, default: int = 0) -> int:
        v = state.get(key, default)
        try:
            return int(v)
        except Exception:
            return default

    def p_optimist(state: Mapping[str, Any], step: int) -> Opinion:
        target = _get_int(state, "target", 0)
        return Opinion("optimist", {"x_target": target + 1}, 0.60, "Slightly above target")

    def p_realist(state: Mapping[str, Any], step: int) -> Opinion:
        target = _get_int(state, "target", 0)
        return Opinion("realist", {"x_target": target}, 0.70, "Exact target")

    def p_cautious(state: Mapping[str, Any], step: int) -> Opinion:
        x = _get_int(state, "x", 0)
        target = _get_int(state, "target", 0)
        mid = int((x + target) / 2)
        return Opinion("cautious", {"x_target": mid}, 0.65, "Midpoint between x and target")

    def p_pessimist(state: Mapping[str, Any], step: int) -> Opinion:
        target = _get_int(state, "target", 0)
        return Opinion("pessimist", {"x_target": target - 1}, 0.55, "Slightly below target")

    # Orden fijo (importante para determinismo si alguien lo usa directo)
    return [p_optimist, p_realist, p_cautious, p_pessimist]
