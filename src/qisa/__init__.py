from __future__ import annotations


from .engine import FixpointResult, run_fixpoint


from .operators import make_perspective_operator


from .perspectives import Opinion, Perspective


from .traces import trace_to_json, verify_trace


from .types import ConsensusConfig, StepRecord, Trace


from .errors import NonConvergentError


__all__ = [
    "__version__",
    "ConsensusConfig",
    "FixpointResult",
    "make_perspective_operator",
    "NonConvergentError",
    "Opinion",
    "Perspective",
    "run_fixpoint",
    "StepRecord",
    "Trace",
    "trace_to_json",
    "verify_trace",
]


__version__ = "0.0.0"
