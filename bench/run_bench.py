from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from qisa import ConsensusConfig, run_fixpoint
from qisa.traces import trace_to_json

from .baselines import (
    run_majority_vote_binned,
    run_qisa,
    run_single_perspective,
    run_weighted_average,
)
from .scenarios.scenario_numeric_target import SCENARIO, perspectives


def _make_operator(name: str):
    ps = perspectives()
    if name == "qisa":
        return lambda s, step: run_qisa(
            ps,
            s,
            step,
            key=SCENARIO.key,
            proposal_field=SCENARIO.proposal_field,
            state_field=SCENARIO.state_field,
        )
    if name == "single":
        return lambda s, step: run_single_perspective(ps, s, step)
    if name == "weighted_avg":
        return lambda s, step: run_weighted_average(
            ps, s, step, key=SCENARIO.key, state_field=SCENARIO.state_field
        )
    if name == "majority_binned":
        return lambda s, step: run_majority_vote_binned(
            ps, s, step, key=SCENARIO.key, state_field=SCENARIO.state_field
        )
    raise ValueError(f"unknown baseline: {name}")


def run_all() -> dict[str, Any]:
    cfg = ConsensusConfig(max_steps=20, stable_steps_required=2)
    results = {}

    for name in ["qisa", "single", "weighted_avg", "majority_binned"]:
        op = _make_operator(name)
        res = run_fixpoint(
            run_id=f"bench_{SCENARIO.name}_{name}",
            initial_state=SCENARIO.initial_state,
            operator=op,
            config=cfg,
        )
        results[name] = {
            "scenario": asdict(SCENARIO),
            "converged": res.converged,
            "steps": res.steps,
            "final_state": dict(res.final_state),
            "trace_hash": res.trace.trace_hash,
            "records_len": len(res.trace.records),
            "trace": trace_to_json(res.trace),
        }

    return results


def main() -> None:
    out = run_all()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
