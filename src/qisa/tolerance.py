# --- Backwards-compatible config name ----------------------------------------
# Some external callers/tests expect ToleranceConfig to exist in qisa.tolerance.
# We provide a stable dataclass wrapper that can be used by the engine.
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToleranceConfig:
    """
    Minimal, stable tolerance configuration for deterministic fixpoint runs.

    Notes:
    - Keep defaults conservative and deterministic.
    - If the engine evolves, keep this class as a compatibility surface.
    """

    max_steps: int = 64
    stable_steps_required: int = 2
    eps: float = 0.0  # convergence tolerance; 0.0 means exact equality


# -----------------------------------------------------------------------------
