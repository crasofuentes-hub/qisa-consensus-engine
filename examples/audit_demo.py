from __future__ import annotations

import json

from qisa import (
    ConsensusConfig,
    make_perspective_operator,
    run_fixpoint,
    trace_to_json,
    verify_trace,
)
from qisa.perspectives import Opinion


def p_fast(state, step):
    return Opinion("p_fast", {"x_target": 2}, 0.7, "Fast convergence preference")


def p_safe(state, step):
    return Opinion("p_safe", {"x_target": 0}, 0.6, "Conservative preference")


p_fast.perspective_id = "p_fast"
p_safe.perspective_id = "p_safe"


def main() -> None:
    cfg = ConsensusConfig(max_steps=10, stable_steps_required=2)
    op = make_perspective_operator([p_safe, p_fast], key="x_target")
    res = run_fixpoint(run_id="audit_demo", initial_state={"x": 1}, operator=op, config=cfg)

    print("Converged:", res.converged)
    print("Final state:", dict(res.final_state))
    print("Trace hash:", res.trace.trace_hash)
    print("Verify trace:", verify_trace(res.trace))

    payload = trace_to_json(res.trace)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
