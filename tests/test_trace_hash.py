from __future__ import annotations

from qisa import ConsensusConfig, run_fixpoint
from qisa.traces import hash_step, sha256_hex, zero_hash


def _decay_to_zero_operator(state: dict, step: int):
    x = int(state.get("x", 0))
    new_x = x - 1 if x > 0 else 0
    new_state = {"x": new_x}
    decision = {"action": "decrement" if x > 0 else "hold", "x": new_x, "step": step}
    return new_state, decision


def test_step_hash_chain_is_deterministic():
    cfg = ConsensusConfig(max_steps=20, stable_steps_required=2)
    r1 = run_fixpoint(
        run_id="t_chain_1", initial_state={"x": 3}, operator=_decay_to_zero_operator, config=cfg
    )
    r2 = run_fixpoint(
        run_id="t_chain_2", initial_state={"x": 3}, operator=_decay_to_zero_operator, config=cfg
    )

    assert r1.trace.trace_hash == r2.trace.trace_hash
    assert len(r1.trace.records) == len(r2.trace.records)


def test_chain_detects_tampering_in_intermediate_record():
    cfg = ConsensusConfig(max_steps=20, stable_steps_required=2)
    res = run_fixpoint(
        run_id="t_tamper", initial_state={"x": 3}, operator=_decay_to_zero_operator, config=cfg
    )
    recs = res.trace.records
    assert len(recs) >= 2

    # Recompute chain but tamper a decision at step 1 (without changing state_hash)
    prev = zero_hash()
    for rec in recs:
        if rec.step == 1:
            tampered_decision_hash = sha256_hex({"action": "tampered", "x": 999, "step": 1})
            h = hash_step(
                step=rec.step,
                state_hash=rec.state_hash,
                decision_hash=tampered_decision_hash,
                prev_step_hash=prev,
            )
        else:
            h = hash_step(
                step=rec.step,
                state_hash=rec.state_hash,
                decision_hash=rec.decision_hash,
                prev_step_hash=prev,
            )
        prev = h

    # The resulting chain hash must differ from the stored trace_hash
    assert prev != res.trace.trace_hash
