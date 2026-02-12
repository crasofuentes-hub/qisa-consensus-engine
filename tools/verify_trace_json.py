from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from qisa import StepRecord, Trace, verify_trace


def _require(d: Mapping[str, Any], key: str) -> Any:
    if key not in d:
        raise ValueError(f"Missing required key: {key}")
    return d[key]


def load_trace_json(path: Path) -> Trace:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("Trace JSON must be an object")

    run_id = str(_require(obj, "run_id"))
    input_hash = str(_require(obj, "input_hash"))
    output_hash = str(_require(obj, "output_hash"))
    trace_hash = str(_require(obj, "trace_hash"))
    records_raw = _require(obj, "records")

    if not isinstance(records_raw, list):
        raise ValueError("records must be a list")

    records = []
    for i, r in enumerate(records_raw):
        if not isinstance(r, dict):
            raise ValueError(f"records[{i}] must be an object")

        rec = StepRecord(
            step=int(_require(r, "step")),
            state=_require(r, "state"),
            decision=_require(r, "decision"),
            state_hash=str(_require(r, "state_hash")),
            decision_hash=str(_require(r, "decision_hash")),
            prev_step_hash=str(_require(r, "prev_step_hash")),
            step_hash=str(_require(r, "step_hash")),
        )
        records.append(rec)

    return Trace(
        run_id=run_id,
        input_hash=input_hash,
        records=tuple(records),
        output_hash=output_hash,
        trace_hash=trace_hash,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify QISA trace JSON (external).")
    ap.add_argument(
        "trace_json",
        type=str,
        help="Path to trace JSON produced by qisa.trace_to_json().",
    )
    args = ap.parse_args()

    p = Path(args.trace_json)
    if not p.exists():
        raise SystemExit(f"File not found: {p}")

    trace = load_trace_json(p)
    ok = bool(verify_trace(trace))
    print("VALID" if ok else "INVALID")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
