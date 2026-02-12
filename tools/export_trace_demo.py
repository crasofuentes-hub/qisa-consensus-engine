from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from qisa import ConsensusConfig, run_fixpoint, trace_to_json


def op(state: Mapping[str, Any], step: int):
    # Operador determinista mínimo: converge rápido y produce decisiones
    x = int(state.get("x", 0))
    if x >= 3:
        new_state = dict(state)
        decision = {"choice": "hold", "x_target": x, "coherence": 1.0}
        return new_state, decision

    new_state = dict(state)
    new_state["x"] = x + 1
    decision = {"choice": "inc", "x_target": x + 1, "coherence": 0.9}
    return new_state, decision


def main() -> int:
    out_dir = Path("tools/_artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "trace_demo.json"

    cfg = ConsensusConfig(max_steps=20, stable_steps_required=2)
    result = run_fixpoint(
        run_id="trace_demo",
        initial_state={"x": 0},
        operator=op,
        config=cfg,
    )

    payload = trace_to_json(result.trace)
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print(f"WROTE: {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
