from __future__ import annotations

from qisa import ConsensusConfig, make_perspective_operator, run_fixpoint
from qisa.perspectives import Opinion


def p_fast(state, step):
    # wants x_target=2 quickly
    return Opinion("p_fast", {"x_target": 2}, 0.7, "Fast convergence preference")


def p_safe(state, step):
    # wants x_target=0 (conservative)
    return Opinion("p_safe", {"x_target": 0}, 0.6, "Conservative preference")


def p_bold(state, step):
    # wants x_target=3
    return Opinion("p_bold", {"x_target": 3}, 0.65, "Aggressive preference")


# Attach stable ids for sorting inside operator
p_fast.perspective_id = "p_fast"
p_safe.perspective_id = "p_safe"
p_bold.perspective_id = "p_bold"


def test_consensus_is_order_independent_and_deterministic():
    cfg = ConsensusConfig(max_steps=10, stable_steps_required=2)

    op1 = make_perspective_operator([p_safe, p_fast, p_bold], key="x_target")
    op2 = make_perspective_operator([p_bold, p_safe, p_fast], key="x_target")

    r1 = run_fixpoint(run_id="t_p1", initial_state={"x": 1}, operator=op1, config=cfg)
    r2 = run_fixpoint(run_id="t_p2", initial_state={"x": 1}, operator=op2, config=cfg)

    assert r1.converged is True
    assert r2.converged is True
    assert r1.final_state == r2.final_state
    assert r1.trace.trace_hash == r2.trace.trace_hash
