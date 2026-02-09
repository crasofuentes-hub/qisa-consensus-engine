from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .traces import hash_step, sha256_hex, zero_hash
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

    if cfg.max_steps <= 0:
        raise ValueError("max_steps must be > 0")
    if cfg.stable_steps_required <= 0:
        raise ValueError("stable_steps_required must be > 0")

    state: Mapping[str, Any] = dict(initial_state)
    input_hash = sha256_hex(state)

    records: list[StepRecord] = []
    stable = 0
    prev = zero_hash()

    for step in range(cfg.max_steps):
        new_state, decision = operator(state, step)

        s_hash = sha256_hex(state)
        d_hash = sha256_hex(decision)
        step_hash = hash_step(
            step=step, state_hash=s_hash, decision_hash=d_hash, prev_step_hash=prev
        )

        records.append(
            StepRecord(
                step=step,
                state=dict(state),
                decision=dict(decision),
                state_hash=s_hash,
                decision_hash=d_hash,
                prev_step_hash=prev,
                step_hash=step_hash,
            )
        )

        prev = step_hash

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
                trace_hash=prev,
            )
            return FixpointResult(
                converged=True,
                steps=step + 1,
                final_state=state,
                trace=trace,
            )

    output_hash = sha256_hex(state)
    trace = Trace(
        run_id=run_id,
        input_hash=input_hash,
        records=tuple(records),
        output_hash=output_hash,
        trace_hash=prev,
    )
    return FixpointResult(
        converged=False,
        steps=cfg.max_steps,
        final_state=state,
        trace=trace,
    )
