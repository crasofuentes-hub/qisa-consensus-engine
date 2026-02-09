from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any


def _to_jsonable(obj: Any) -> Any:
    """
    Convert Python objects to JSON-serializable structures deterministically.
    - dataclasses -> dict via asdict
    - tuples -> lists
    - sets -> sorted lists
    - dict keys are kept as-is but final JSON encoding sorts keys
    """
    if is_dataclass(obj):
        return _to_jsonable(asdict(obj))

    if isinstance(obj, dict):
        # Convert values recursively. Keys must be JSON-serializable (strings recommended).
        return {str(k): _to_jsonable(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(x) for x in obj]

    if isinstance(obj, set):
        return sorted([_to_jsonable(x) for x in obj], key=lambda x: json.dumps(x, sort_keys=True))

    return obj


def canonical_json_bytes(payload: Any) -> bytes:
    """
    Stable JSON encoding:
    - sort_keys=True ensures deterministic key order
    - separators remove whitespace differences
    - ensure_ascii=False keeps unicode stable
    """
    jsonable = _to_jsonable(payload)
    s = json.dumps(jsonable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return s.encode("utf-8")


def sha256_hex(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
