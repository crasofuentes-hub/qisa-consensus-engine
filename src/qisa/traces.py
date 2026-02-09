from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any


def _to_jsonable(obj: Any) -> Any:
    if is_dataclass(obj):
        return _to_jsonable(asdict(obj))

    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(x) for x in obj]

    if isinstance(obj, set):
        return sorted([_to_jsonable(x) for x in obj], key=lambda x: json.dumps(x, sort_keys=True))

    return obj


def canonical_json_bytes(payload: Any) -> bytes:
    jsonable = _to_jsonable(payload)
    s = json.dumps(jsonable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return s.encode("utf-8")


def sha256_hex(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def zero_hash() -> str:
    return "0" * 64


def hash_step(*, step: int, state_hash: str, decision_hash: str, prev_step_hash: str) -> str:
    payload = {
        "step": step,
        "state_hash": state_hash,
        "decision_hash": decision_hash,
        "prev_step_hash": prev_step_hash,
    }
    return sha256_hex(payload)


from .types import Trace


def trace_to_json(trace: Trace) -> dict:
    return {
        "run_id": trace.run_id,
        "input_hash": trace.input_hash,
        "output_hash": trace.output_hash,
        "trace_hash": trace.trace_hash,
        "records": [
            {
                "step": r.step,
                "state": dict(r.state),
                "decision": dict(r.decision),
                "state_hash": r.state_hash,
                "decision_hash": r.decision_hash,
                "prev_step_hash": r.prev_step_hash,
                "step_hash": r.step_hash,
            }
            for r in trace.records
        ],
    }


def verify_trace(trace: Trace) -> bool:
    prev = zero_hash()
    for r in trace.records:
        # recompute the expected step hash
        expected = hash_step(
            step=r.step,
            state_hash=r.state_hash,
            decision_hash=r.decision_hash,
            prev_step_hash=prev,
        )
        if expected != r.step_hash:
            return False
        if r.prev_step_hash != prev:
            return False
        prev = r.step_hash

    return prev == trace.trace_hash
