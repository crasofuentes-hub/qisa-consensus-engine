from __future__ import annotations

from .engine import FixpointResult, run_fixpoint
from .operators import make_perspective_operator
from .perspectives import Opinion, Perspective
from .types import ConsensusConfig, StepRecord, Trace

__all__ = [
    "ConsensusConfig",
    "FixpointResult",
    "Opinion",
    "Perspective",
    "StepRecord",
    "Trace",
    "make_perspective_operator",
    "run_fixpoint",
    "__version__",
]

__version__ = "0.0.0"
