from __future__ import annotations

from collections import Counter
from math import log2
from typing import Any, Mapping, Sequence

from .types import StepRecord, Trace


def disagreement_entropy(decisions: Sequence[Mapping[str, Any]]) -> float:
    """
    Entropía (Shannon) de desacuerdo basada en una clave "choice" si existe;
    si no existe, usa la serialización estable del dict (sorted items).
    Retorna >= 0.0.
    """
    if not decisions:
        return 0.0

    labels: list[str] = []
    for d in decisions:
        if not isinstance(d, Mapping):
            labels.append(str(d))
            continue
        if "choice" in d:
            labels.append(str(d["choice"]))
        else:
            labels.append(str(sorted(d.items(), key=lambda kv: str(kv[0]))))

    c = Counter(labels)
    n = sum(c.values())
    if n <= 0:
        return 0.0

    h = 0.0
    for k in c:
        p = c[k] / n
        if p > 0:
            h -= p * log2(p)
    return h


def numeric_variance(values: Sequence[float]) -> float:
    """Varianza poblacional simple (determinista)."""
    if not values:
        return 0.0
    n = float(len(values))
    mu = sum(values) / n
    return sum((x - mu) ** 2 for x in values) / n


def compute_quality_metrics(
    *,
    trace: Trace | None = None,
    records: Sequence[StepRecord] | None = None,
    decisions: Sequence[Mapping[str, Any]] | None = None,
    final_state: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    API NORMALIZADA.

    - Preferencia de fuente:
        1) trace -> records
        2) records
        3) decisions (+ opcional final_state)

    - Retrocompatible:
        si lo llamas sin argumentos, devuelve {}.
    """
    # Retrocompatibilidad explícita: no args -> {}
    if trace is None and records is None and decisions is None and final_state is None:
        return {}

    if records is None and trace is not None:
        records = trace.records

    if decisions is None and records is not None:
        decisions = [r.decision for r in records]

    if decisions is None:
        decisions = []

    # Métricas base
    ent = disagreement_entropy(decisions)

    # Ejemplo: si hay números en decisions bajo x_target, medimos varianza
    x_targets: list[float] = []
    for d in decisions:
        if isinstance(d, Mapping) and "x_target" in d:
            try:
                x_targets.append(float(d["x_target"]))
            except Exception:
                pass

    var = numeric_variance(x_targets)

    out: dict[str, Any] = {
        "disagreement_entropy": float(ent),
        "x_target_variance": float(var),
        "decision_count": int(len(decisions)),
    }

    # final_state opcional: agregamos un hash/summary determinista mínimo
    if final_state is not None:
        out["final_state_keys"] = sorted([str(k) for k in final_state.keys()])

    return out
