from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Literal


@dataclass(frozen=True, slots=True)
class ConsensusConfig:
    max_steps: int = 32
    stable_steps_required: int = 2  # consecutive no-change steps define fixpoint
    on_non_convergence: Literal["raise", "last"] = "last"


@dataclass(frozen=True, slots=True)
class StepRecord:
    step: int
    state: Mapping[str, Any]
    decision: Mapping[str, Any]
    state_hash: str
    decision_hash: str
    prev_step_hash: str
    step_hash: str


@dataclass(frozen=True, slots=True)
class Trace:
    run_id: str
    input_hash: str
    records: tuple[StepRecord, ...]
    output_hash: str
    trace_hash: str
