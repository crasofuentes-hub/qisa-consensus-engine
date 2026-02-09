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
