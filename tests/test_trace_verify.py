from __future__ import annotations

from qisa import ConsensusConfig, make_perspective_operator, run_fixpoint, verify_trace
from qisa.perspectives import Opinion


def p1(state, step):
    return Opinion("p1", {"x_target": 2}, 0.7, "p1")


def p2(state, step):
    return Opinion("p2", {"x_target": 0}, 0.6, "p2")


p1.perspective_id = "p1"
p2.perspective_id = "p2"


def test_verify_trace_ok_for_authentic_trace():
    cfg = ConsensusConfig(max_steps=10, stable_steps_required=2)
    op = make_perspective_operator([p2, p1], key="x_target")
    res = run_fixpoint(run_id="t_verify_ok", initial_state={"x": 1}, operator=op, config=cfg)
    assert verify_trace(res.trace) is True


def test_verify_trace_fails_if_record_is_tampered():
    cfg = ConsensusConfig(max_steps=10, stable_steps_required=2)
    op = make_perspective_operator([p2, p1], key="x_target")
    res = run_fixpoint(run_id="t_verify_bad", initial_state={"x": 1}, operator=op, config=cfg)

    # Tamper: change stored decision_hash on first record (simulate corruption)
    rec0 = res.trace.records[0]
    tampered = type(rec0)(
        step=rec0.step,
        state=rec0.state,
        decision=rec0.decision,
        state_hash=rec0.state_hash,
        decision_hash="f" * 64,
        prev_step_hash=rec0.prev_step_hash,
        step_hash=rec0.step_hash,
    )

    new_records = (tampered,) + tuple(res.trace.records[1:])
    trace2 = type(res.trace)(
        run_id=res.trace.run_id,
        input_hash=res.trace.input_hash,
        records=new_records,
        output_hash=res.trace.output_hash,
        trace_hash=res.trace.trace_hash,
    )

    assert verify_trace(trace2) is False
