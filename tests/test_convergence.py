from __future__ import annotations

from qisa import ConsensusConfig, run_fixpoint


def _decay_to_zero_operator(state: dict, step: int):
    x = int(state.get("x", 0))
    new_x = x - 1 if x > 0 else 0
    new_state = {"x": new_x}
    decision = {"action": "decrement" if x > 0 else "hold", "x": new_x, "step": step}
    return new_state, decision


def test_converges_to_fixpoint():
    cfg = ConsensusConfig(max_steps=50, stable_steps_required=2)
    res = run_fixpoint(
        run_id="t_converge",
        initial_state={"x": 5},
        operator=_decay_to_zero_operator,
        config=cfg,
    )
    assert res.converged is True
    assert res.final_state["x"] == 0
    assert res.steps <= cfg.max_steps
    assert res.trace.input_hash
    assert res.trace.output_hash
    assert len(res.trace.records) >= 1
