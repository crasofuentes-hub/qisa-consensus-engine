from dataclasses import dataclass

from qisa.consensus import choose_consensus


@dataclass(frozen=True)
class _Opinion:
    choice: str
    proposal: dict
    confidence: float = 1.0
    perspective_id: str = "p0"


def test_choose_consensus_ties_and_empty():
    import pytest

    # vacío -> contrato: debe fallar explícitamente
    with pytest.raises(ValueError):
        choose_consensus([], key="choice")

    # empate -> debe resolver determinísticamente (por score/tie-break)


o1 = _Opinion(choice="a", proposal={"x_target": 1}, confidence=1.0, perspective_id="p1")
o2 = _Opinion(choice="b", proposal={"x_target": 1}, confidence=1.0, perspective_id="p2")
out = choose_consensus([o1, o2], key="x_target")
# contrato real: choose_consensus devuelve ConsensusDecision (no dict)
assert hasattr(out, "decision")
assert isinstance(out.decision, dict)
assert out.decision.get("x_target") == 1
# opcional: sanity checks del objeto
assert hasattr(out, "chosen_perspective_id")
assert hasattr(out, "coherence")
