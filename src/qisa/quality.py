from __future__ import annotations

from collections import Counter
from math import log2
from typing import Any, Mapping


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def disagreement_entropy(values: list[Any]) -> float:
    """
    Shannon entropy over discrete values.
    Deterministic for a fixed list order (Counter ignores order; stable via sorted keys).
    """
    if not values:
        return 0.0
    c = Counter(values)
    total = sum(c.values())
    if total <= 0:
        return 0.0

    # stable ordering
    items = sorted(c.items(), key=lambda kv: repr(kv[0]))
    h = 0.0
    for _, cnt in items:
        p = cnt / total
        if p > 0:
            h -= p * log2(p)
    return h


def numeric_variance(values: list[float]) -> float:
    if not values:
        return 0.0
    n = float(len(values))
    mean = sum(values) / n
    return sum((v - mean) ** 2 for v in values) / n


def compute_quality_metrics(
    *,
    initial_state: Mapping[str, Any],
    final_state: Mapping[str, Any],
    last_decision: Mapping[str, Any] | None,
    per_key_proposals: Mapping[str, list[Any]] | None = None,
) -> dict[str, Any]:
    """
    Minimal, production-useful quality metrics.

    - changed_keys_ratio: how much the final state differs from initial (by key equality)
    - mean_coherence: if decision provides 'coherence'
    - per_key_entropy: entropy over proposals per key (if provided)
    - per_key_variance: variance over numeric proposals per key (if provided)
    """
    keys = sorted(set(initial_state.keys()) | set(final_state.keys()))
    changed = 0
    for k in keys:
        if initial_state.get(k) != final_state.get(k):
            changed += 1
    changed_keys_ratio = (changed / len(keys)) if keys else 0.0

    mean_coherence = None
    if isinstance(last_decision, Mapping) and "coherence" in last_decision:
        try:
            mean_coherence = float(last_decision["coherence"])
        except Exception:
            mean_coherence = None

    per_key_entropy: dict[str, float] = {}
    per_key_variance: dict[str, float] = {}

    if per_key_proposals:
        for k in sorted(per_key_proposals.keys()):
            vals = list(per_key_proposals[k])
            per_key_entropy[k] = disagreement_entropy(vals)

            num = [float(v) for v in vals if _is_number(v)]
            if num:
                per_key_variance[k] = numeric_variance(num)

    out: dict[str, Any] = {
        "changed_keys_ratio": changed_keys_ratio,
    }
    if mean_coherence is not None:
        out["mean_coherence"] = mean_coherence
    if per_key_entropy:
        out["per_key_entropy"] = per_key_entropy
    if per_key_variance:
        out["per_key_variance"] = per_key_variance
    return out
