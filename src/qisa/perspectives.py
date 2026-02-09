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

# --- Public factory: default perspectives ------------------------------------
# Backwards-compatible entrypoint used by property tests and external callers.
# This is intentionally robust to Perspective signature changes (name/id, weight/w, etc.).


def make_default_perspectives():
    """
    Returns a canonical, deterministic set of default perspectives.

    We intentionally build kwargs by introspecting Perspective.__init__ to avoid
    brittle coupling to field names (e.g., name vs id, weight vs w).
    """
    import inspect

    try:
        sig = inspect.signature(Perspective)
        params = set(sig.parameters.keys())
    except Exception:
        # If Perspective is not introspectable for any reason, fall back to simplest shape.
        params = {"name", "weight"}

    def _mk(name: str, weight: float = 1.0):
        kwargs = {}
        if "name" in params:
            kwargs["name"] = name
        elif "id" in params:
            kwargs["id"] = name

        if "weight" in params:
            kwargs["weight"] = weight
        elif "w" in params:
            kwargs["w"] = weight

        # If the class expects more params, they must already have defaults.
        return Perspective(**kwargs)

    return [
        _mk("optimist", 1.0),
        _mk("skeptic", 1.0),
        _mk("risk_averse", 1.0),
    ]


from typing import Any, Callable, Mapping

# -----------------------------------------------------------------------------
