from __future__ import annotations

from qisa.traces import sha256_hex


def test_sha256_is_deterministic_for_equivalent_dicts():
    a = {"x": 1, "y": {"z": [3, 2, 1]}}
    b = {"y": {"z": [3, 2, 1]}, "x": 1}  # same content, different key order
    assert sha256_hex(a) == sha256_hex(b)


def test_sha256_changes_when_payload_changes():
    a = {"x": 1, "y": {"z": [3, 2, 1]}}
    b = {"x": 1, "y": {"z": [3, 2, 9]}}
    assert sha256_hex(a) != sha256_hex(b)
