from hypothesis import given, settings
from hypothesis.strategies import integers

from qisa import make_perspective_operator, run_fixpoint
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
    op = make_perspective_operator(perspectives, key="x_target")

    r1 = run_fixpoint(run_id="prop_det_1", initial_state=state, operator=op, config=cfg)
    r2 = run_fixpoint(run_id="prop_det_2", initial_state=state, operator=op, config=cfg)

    # Prefer trace_hash if present; otherwise fallback to trace.output_hash
    if hasattr(r1, "trace_hash") and hasattr(r2, "trace_hash"):
        assert r1.trace_hash == r2.trace_hash
    else:
        assert r1.trace.output_hash == r2.trace.output_hash
