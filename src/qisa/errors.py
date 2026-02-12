from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class NonConvergentError(RuntimeError):
    run_id: str
    max_steps: int
    stable_steps_required: int
    steps: int
    last_state: Mapping[str, Any]
    trace_hash: str
    stop_reason: str = "max_steps_exceeded"

    def __str__(self) -> str:
        return (
            "NonConvergentError("
            f"run_id={self.run_id!r}, "
            f"stop_reason={self.stop_reason!r}, "
            f"steps={self.steps}, "
            f"max_steps={self.max_steps}, "
            f"stable_steps_required={self.stable_steps_required}, "
            f"trace_hash={self.trace_hash}"
            ")"
        )
