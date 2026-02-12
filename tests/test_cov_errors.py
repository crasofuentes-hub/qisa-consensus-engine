import pytest

from qisa import ConsensusConfig, NonConvergentError, run_fixpoint


def _never_converge(state, step):
    # Siempre cambia, nunca se estabiliza
    x = int(state.get("x", 0))
    return {"x": x + 1}, {"x_target": x + 1, "choice": "nc"}


def test_nonconvergent_raise_path_hits_error_line():
    cfg = ConsensusConfig(max_steps=3, stable_steps_required=2, on_non_convergence="raise")
    with pytest.raises(NonConvergentError):
        run_fixpoint(
            run_id="cov_raise", initial_state={"x": 0}, operator=_never_converge, config=cfg
        )
