from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | Mapping[str, "JsonValue"] | Sequence["JsonValue"]


@dataclass(frozen=True, slots=True)
class ConsensusConfig:
    max_steps: int = 32
    stable_steps_required: int = 2  # how many consecutive "no-change" steps define fixpoint


@dataclass(frozen=True, slots=True)
class StepRecord:
    step: int
    state: Mapping[str, Any]
    decision: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class Trace:
    run_id: str
    input_hash: str
    records: tuple[StepRecord, ...]
    output_hash: str
