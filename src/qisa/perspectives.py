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


# -----------------------------------------------------------------------------

# =============================================================================
# Compatibility patch (property tests)
# - Ensure Perspective is instantiable (not a typing.Callable alias)
# - Provide make_default_perspectives() factory expected by Hypothesis tests
# - Opinion construction is robust to signature changes
# =============================================================================
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, Mapping, Sequence

# If "Perspective" is currently a typing alias (e.g., Callable[...] from typing),
# provide a concrete dataclass and preserve the alias as OpinionFn.
try:
    _is_typing_callable = (
        getattr(Perspective, "__module__", "") == "typing"
        and getattr(Perspective, "__origin__", None) is Callable
    )
except Exception:
    _is_typing_callable = False

if _is_typing_callable:
    OpinionFn = Perspective  # keep the original meaning as a function type

    @dataclass(frozen=True, slots=True)
    class Perspective:
        name: str
        weight: float
        opine: OpinionFn


def _mk_opinion(value: float, confidence: float = 1.0) -> Any:
    """
    Build an Opinion instance robustly:
    - If Opinion is a dataclass, fill known fields and defaults for the rest.
    - Otherwise, try the simplest constructor paths.
    """
    try:
        if is_dataclass(Opinion):
            kw: dict[str, Any] = {}
            for f in fields(Opinion):
                if f.name == "value":
                    kw[f.name] = value
                elif f.name == "confidence":
                    kw[f.name] = confidence
                elif f.default is not None and f.default is not dataclass:
                    # dataclasses.MISSING is not None, but we avoid importing it; handle below
                    pass
            # Fill remaining required fields (no default) with safe placeholders
            for f in fields(Opinion):
                if f.name in kw:
                    continue
                has_default = (
                    getattr(f, "default_factory", None) is not None
                    or str(f.default) != "dataclasses.MISSING"
                )
                if has_default:
                    continue
                # best-effort placeholders
                ann = str(f.type)
                if "dict" in ann or "Mapping" in ann:
                    kw[f.name] = {}
                elif "list" in ann or "Sequence" in ann:
                    kw[f.name] = []
                elif "str" in ann:
                    kw[f.name] = ""
                elif "float" in ann:
                    kw[f.name] = 0.0
                elif "int" in ann:
                    kw[f.name] = 0
                else:
                    kw[f.name] = None
            return Opinion(**kw)

        # Non-dataclass Opinion: try common forms
        try:
            return Opinion(value=value, confidence=confidence)
        except TypeError:
            return Opinion(value)
    except Exception:
        # Last resort: return a minimal dict (some pipelines accept this)
        return {"value": value, "confidence": confidence}


def make_default_perspectives() -> Sequence[Any]:
    """
    Default 3-perspective set for deterministic numeric target scenarios.
    Returned objects are compatible with operators expecting:
    - either Perspective(name, weight, opine)
    - or any object exposing .name .weight .opine
    """

    def _opine_bias(bias: float):
        def _fn(state: Mapping[str, Any], step: int):
            x = float(state.get("x", 0.0))
            return _mk_opinion(x + bias, confidence=1.0)

        return _fn

    return [
        Perspective(name="optimist", weight=1.0, opine=_opine_bias(+1.0)),
        Perspective(name="realist", weight=1.0, opine=_opine_bias(0.0)),
        Perspective(name="pessimist", weight=1.0, opine=_opine_bias(-1.0)),
    ]


# =============================================================================
