from __future__ import annotations

from hypothesis import given, settings
from hypothesis.strategies import integers

from qisa.engine import run_fixpoint
from qisa.operators import deterministic_consensus_operator
from qisa.perspectives import make_default_perspectives
from qisa.tolerance import ToleranceConfig


@settings(max_examples=80, deadline=None)
@given(x=integers(min_value=-50, max_value=50), target=integers(min_value=-50, max_value=50))
def test_determinism_same_inputs_same_trace_hash(x: int, target: int) -> None:
    """
    Property: given identical inputs/config, the full trace hash must be identical.
    This is stronger than "same final_state" because it constrains every step.
    """
    state = {"x": x, "target": target}

    cfg = ToleranceConfig(max_steps=12)

    perspectives = make_default_perspectives()

    r1 = run_fixpoint(
        initial_state=state,
        perspectives=perspectives,
        operator=deterministic_consensus_operator,
        config=cfg,
    )

    r2 = run_fixpoint(
        initial_state=state,
        perspectives=perspectives,
        operator=deterministic_consensus_operator,
        config=cfg,
    )

    assert r1.converged is True
    assert r2.converged is True
    assert r1.final_state == r2.final_state
    assert r1.trace.output_hash == r2.trace.output_hash
