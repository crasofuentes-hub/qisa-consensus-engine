from __future__ import annotations

import json
from pathlib import Path


def test_results_artifact_exists_and_has_expected_keys():
    p = Path("bench/results_scenario_v1.json")
    assert p.exists(), "Run: python -m bench.run_bench > bench/results_scenario_v1.json"
    data = json.loads(p.read_text(encoding="utf-8-sig"))

    for k in ["qisa", "single", "weighted_avg", "majority_binned"]:
        assert k in data
        assert "trace_hash" in data[k]
        assert "final_state" in data[k]
