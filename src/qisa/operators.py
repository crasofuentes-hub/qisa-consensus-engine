from typing import Any, Mapping, Protocol, Sequence

from .consensus import choose_consensus
from .perspectives import Perspective


class ConsensusOperator(Protocol):
    def __call__(
        self, state: Mapping[str, Any], step: int
    ) -> tuple[Mapping[str, Any], Mapping[str, Any]]: ...


def __call__(
    self, state: Mapping[str, Any], step: int
) -> tuple[Mapping[str, Any], Mapping[str, Any]]: ...


def make_perspective_operator(
    perspectives: Sequence[Perspective],
    *,
    key: str,
    state_field: str = "x",
    proposal_field: str = "x_target",
):
    """
    Build a deterministic ConsensusOperator for run_fixpoint.
    - perspectives are evaluated in deterministic order by perspective_id (stable)
    - decision is derived by choose_consensus
    - new_state updates `state_field` toward proposal_field
    """

    # Enforce deterministic ordering regardless of caller order:
    # we evaluate each perspective once to read its id? We can't without running it.
    # So we require each Perspective closure to have attribute 'perspective_id' for sorting.
    def _sorted_perspectives():
        def pid(p: Perspective) -> str:
            return getattr(p, "perspective_id", p.__name__)

        return sorted(list(perspectives), key=pid)

    def operator(state: Mapping[str, Any], step: int):
        ops = []
        for p in _sorted_perspectives():
            o = p(state, step)
            ops.append(o)

        dec = choose_consensus(ops, key=key)

        current = state.get(state_field, 0)
        target = dec.decision.get(proposal_field, current)

        new_state = dict(state)
        new_state[state_field] = target

        decision_payload = {
            "chosen": dec.chosen_perspective_id,
            "coherence": dec.coherence,
            "proposal": dict(dec.decision),
        }
        return new_state, decision_payload

    return operator


# Backwards-compatible alias used by property tests and external callers.
# This intentionally points to the canonical builder.
deterministic_consensus_operator = make_perspective_operator
