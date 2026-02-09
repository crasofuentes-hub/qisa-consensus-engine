from __future__ import annotations

from bench.run_bench import run_all


def test_bench_is_deterministic():
    a = run_all()
    b = run_all()
    assert a["qisa"]["trace_hash"] == b["qisa"]["trace_hash"]
    assert a["qisa"]["final_state"] == b["qisa"]["final_state"]
