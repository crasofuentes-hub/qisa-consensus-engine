from __future__ import annotations

from qisa import ConsensusConfig, run_fixpoint


def _decay_to_zero_operator(state: dict, step: int):
    x = int(state.get("x", 0))
    new_x = x - 1 if x > 0 else 0
    new_state = {"x": new_x}
    decision = {"action": "decrement" if x > 0 else "hold", "x": new_x, "step": step}
    return new_state, decision


def test_fixpoint_is_idempotent():
    cfg = ConsensusConfig(max_steps=10, stable_steps_required=2)
    res1 = run_fixpoint(
        run_id="t_idem_1",
        initial_state={"x": 0},
        operator=_decay_to_zero_operator,
        config=cfg,
    )
    assert res1.converged is True
    assert res1.final_state == {"x": 0}

    res2 = run_fixpoint(
        run_id="t_idem_2",
        initial_state=res1.final_state,
        operator=_decay_to_zero_operator,
        config=cfg,
    )
    assert res2.converged is True
    assert res2.final_state == res1.final_state
    assert res2.trace.output_hash == res1.trace.output_hash
