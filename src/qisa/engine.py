from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .traces import sha256_hex
from .types import ConsensusConfig, StepRecord, Trace


@dataclass(frozen=True, slots=True)
class FixpointResult:
    converged: bool
    steps: int
    final_state: Mapping[str, Any]
    trace: Trace


ConsensusOperator = Callable[[Mapping[str, Any], int], tuple[Mapping[str, Any], Mapping[str, Any]]]


def run_fixpoint(
    *,
    run_id: str,
    initial_state: Mapping[str, Any],
    operator: ConsensusOperator,
    config: ConsensusConfig | None = None,
) -> FixpointResult:
    cfg = config or ConsensusConfig()

    # Defensive checks (no assumptions)
    if cfg.max_steps <= 0:
        raise ValueError("max_steps must be > 0")
    if cfg.stable_steps_required <= 0:
        raise ValueError("stable_steps_required must be > 0")

    state: Mapping[str, Any] = dict(initial_state)
    input_hash = sha256_hex(state)

    records: list[StepRecord] = []
    stable = 0

    for step in range(cfg.max_steps):
        new_state, decision = operator(state, step)

        records.append(
            StepRecord(
                step=step,
                state=dict(state),
                decision=dict(decision),
            )
        )

        if dict(new_state) == dict(state):
            stable += 1
        else:
            stable = 0

        state = dict(new_state)

        if stable >= cfg.stable_steps_required:
            output_hash = sha256_hex(state)
            trace = Trace(
                run_id=run_id,
                input_hash=input_hash,
                records=tuple(records),
                output_hash=output_hash,
            )
            return FixpointResult(
                converged=True,
                steps=step + 1,
                final_state=state,
                trace=trace,
            )

    # Not converged within max_steps
    output_hash = sha256_hex(state)
    trace = Trace(
        run_id=run_id,
        input_hash=input_hash,
        records=tuple(records),
        output_hash=output_hash,
    )
    return FixpointResult(
        converged=False,
        steps=cfg.max_steps,
        final_state=state,
        trace=trace,
    )
