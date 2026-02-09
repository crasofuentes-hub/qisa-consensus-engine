from __future__ import annotations

from copy import deepcopy

from hypothesis import given, settings
from hypothesis.strategies import integers

from qisa.engine import run_fixpoint
from qisa.operators import deterministic_consensus_operator
from qisa.perspectives import make_default_perspectives
from qisa.tolerance import ToleranceConfig
from qisa.traces import verify_trace


@settings(max_examples=60, deadline=None)
@given(x=integers(min_value=-25, max_value=25), target=integers(min_value=-25, max_value=25))
def test_trace_verification_detects_tampering(x: int, target: int) -> None:
    """
    Property: if any trace record is modified post-hoc, verify_trace must fail.
    """
    state = {"x": x, "target": target}

    cfg = ToleranceConfig(max_steps=12)
    perspectives = make_default_perspectives()

    res = run_fixpoint(
        initial_state=state,
        perspectives=perspectives,
        operator=deterministic_consensus_operator,
        config=cfg,
    )

    assert res.converged is True

    # First: authentic trace verifies
    assert verify_trace(res.trace) is True

    # Now tamper with a copy: mutate a record payload but keep hashes unchanged
    tampered = deepcopy(res.trace)
    assert len(tampered.records) > 0
    tampered.records[0].decision["value"] = tampered.records[0].decision["value"] + 1

    assert verify_trace(tampered) is False
