from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .perspectives import Opinion


def _extract_numeric(proposal: Mapping[str, Any], key: str) -> float:
    v = proposal.get(key, 0)
    try:
        return float(v)
    except Exception as e:  # pragma: no cover
        raise TypeError(f"proposal[{key!r}] must be numeric") from e


def coherence_score(opinions: Sequence[Opinion], key: str) -> float:
    """
    Deterministic coherence proxy (v1):
    coherence = 1 / (1 + mean pairwise abs distance on a numeric key)
    """
    n = len(opinions)
    if n <= 1:
        return 1.0

    vals = [_extract_numeric(o.proposal, key) for o in opinions]
    total = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += abs(vals[i] - vals[j])
            count += 1
    mean_dist = total / float(count)
    return 1.0 / (1.0 + mean_dist)


@dataclass(frozen=True, slots=True)
class ConsensusDecision:
    chosen_perspective_id: str
    decision: Mapping[str, Any]
    coherence: float


def choose_consensus(opinions: Sequence[Opinion], *, key: str) -> ConsensusDecision:
    if not opinions:
        raise ValueError("opinions must be non-empty")

    coh = coherence_score(opinions, key=key)

    # Score each opinion deterministically; tie-break by perspective_id (stable)
    scored = []
    for o in opinions:
        score = float(o.confidence) * float(coh)
        scored.append((score, o.perspective_id, o))

    scored.sort(key=lambda t: (-t[0], t[1]))  # highest score, then lexicographic id

    best = scored[0][2]
    return ConsensusDecision(
        chosen_perspective_id=best.perspective_id,
        decision=dict(best.proposal),
        coherence=coh,
    )
