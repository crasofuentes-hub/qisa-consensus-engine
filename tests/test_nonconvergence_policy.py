import pytest

from qisa import ConsensusConfig, NonConvergentError, run_fixpoint


def _never_converge_operator(state, step):
    # Always changes state to avoid stability
    x = int(state.get("x", 0))
    return {"x": x + 1}, {"chosen": "inc", "coherence": 0.0, "proposal": {"x": x + 1}}


def test_on_non_convergence_raise():
    cfg = ConsensusConfig(max_steps=5, stable_steps_required=2, on_non_convergence="raise")
    with pytest.raises(NonConvergentError):
        run_fixpoint(
            run_id="nc_raise", initial_state={"x": 0}, operator=_never_converge_operator, config=cfg
        )


def test_on_non_convergence_last_returns_result():
    cfg = ConsensusConfig(max_steps=5, stable_steps_required=2, on_non_convergence="last")
    res = run_fixpoint(
        run_id="nc_last", initial_state={"x": 0}, operator=_never_converge_operator, config=cfg
    )
    assert res.converged is False
    assert res.stop_reason == "max_steps_exceeded"
    assert isinstance(res.quality_metrics, dict)
