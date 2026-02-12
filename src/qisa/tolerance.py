from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


OnNonConvergence = Literal["raise", "last", "best_effort", "partial"]


@dataclass(frozen=True)
class ToleranceConfig:
    """
    Core convergence controls.

    - max_steps: hard bound on iterations.
    - eps: tolerance used by operators/perspectives (when applicable).
    - stable_steps_required: number of consecutive stable steps to declare convergence.
    - on_non_convergence: policy when convergence is not reached.
    - oscillation_window: cycle detection window for repeated state hashes.
    """

    max_steps: int = 20
    eps: float = 1e-9
    stable_steps_required: int = 2

    on_non_convergence: OnNonConvergence = "raise"
    oscillation_window: int = 6
