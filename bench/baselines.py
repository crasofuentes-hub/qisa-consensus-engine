from __future__ import annotations

from typing import Any, Mapping, Sequence

from qisa.consensus import choose_consensus
from qisa.perspectives import Opinion, Perspective


def run_single_perspective(
    perspectives: Sequence[Perspective], state: Mapping[str, Any], step: int
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    p = sorted(list(perspectives), key=lambda x: getattr(x, "perspective_id", x.__name__))[0]
    o = p(state, step)
    return state_update_from_opinion(state, o), {
        "baseline": "single",
        "chosen": o.perspective_id,
        "proposal": dict(o.proposal),
    }


def run_weighted_average(
    perspectives: Sequence[Perspective],
    state: Mapping[str, Any],
    step: int,
    *,
    key: str,
    state_field: str,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    ops = [p(state, step) for p in perspectives]
    total_w = sum(float(o.confidence) for o in ops) or 1.0
    avg = sum(float(o.proposal.get(key, 0)) * float(o.confidence) for o in ops) / total_w
    new_state = dict(state)
    new_state[state_field] = avg
    return new_state, {"baseline": "weighted_avg", "value": avg, "n": len(ops)}


def run_majority_vote_binned(
    perspectives: Sequence[Perspective],
    state: Mapping[str, Any],
    step: int,
    *,
    key: str,
    state_field: str,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    # Deterministic binning to ints
    ops = [p(state, step) for p in perspectives]
    votes = {}
    for o in ops:
        v = int(round(float(o.proposal.get(key, 0))))
        votes[v] = votes.get(v, 0) + 1
    # choose max votes, tie-break by smallest value (deterministic)
    chosen = sorted(votes.items(), key=lambda t: (-t[1], t[0]))[0][0]
    new_state = dict(state)
    new_state[state_field] = chosen
    return new_state, {"baseline": "majority_binned", "value": chosen, "votes": dict(votes)}


def run_qisa(
    perspectives: Sequence[Perspective],
    state: Mapping[str, Any],
    step: int,
    *,
    key: str,
    proposal_field: str,
    state_field: str,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    ops = [p(state, step) for p in perspectives]
    dec = choose_consensus(ops, key=key)
    target = dec.decision.get(proposal_field, state.get(state_field, 0))
    new_state = dict(state)
    new_state[state_field] = target
    return new_state, {
        "chosen": dec.chosen_perspective_id,
        "coherence": dec.coherence,
        "proposal": dict(dec.decision),
    }


def state_update_from_opinion(
    state: Mapping[str, Any],
    o: Opinion,
    *,
    state_field: str = "x",
    proposal_field: str = "x_target",
):
    new_state = dict(state)
    new_state[state_field] = o.proposal.get(proposal_field, state.get(state_field, 0))
    return new_state
