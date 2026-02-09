from copy import deepcopy
from dataclasses import replace

from hypothesis import given, settings
from hypothesis.strategies import integers

from qisa import make_perspective_operator, run_fixpoint, verify_trace
from qisa.perspectives import make_default_perspectives
from qisa.tolerance import ToleranceConfig


@settings(max_examples=60, deadline=None)
@given(x=integers(min_value=-25, max_value=25), target=integers(min_value=-25, max_value=25))
def test_trace_verification_detects_tampering(x: int, target: int) -> None:
    """
    Property: if any trace record is modified post-hoc, verify_trace must fail.
    """
    state = {"x": x, "target": target}
    cfg = ToleranceConfig(max_steps=12, stable_steps_required=2)

    perspectives = make_default_perspectives()
    op = make_perspective_operator(perspectives, key="x_target")

    res = run_fixpoint(run_id="prop_tamper", initial_state=state, operator=op, config=cfg)

    # Authentic trace verifies
    assert verify_trace(res.trace) is True

    # Tamper: Trace is dataclass, records is tuple, StepRecord is frozen => rebuild immutably
    tampered = deepcopy(res.trace)
    assert hasattr(tampered, "records")
    assert len(tampered.records) > 0

    new_first = replace(tampered.records[0], state_hash="00" * 32)
    new_records = (new_first,) + tuple(tampered.records[1:])

    tampered = replace(tampered, records=new_records)

    assert verify_trace(tampered) is False
