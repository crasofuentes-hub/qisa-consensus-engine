from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    p = Path("bench/results_scenario_v1.json")
    data = json.loads(p.read_text(encoding="utf-8-sig"))

    order = ["qisa", "single", "weighted_avg", "majority_binned"]

    rows = []
    for k in order:
        r = data[k]
        rows.append(
            {
                "method": k,
                "converged": str(bool(r["converged"])),
                "steps": str(r["steps"]),
                "final_state": json.dumps(r["final_state"], ensure_ascii=False),
                "records": str(r["records_len"]),
                "trace_hash": r["trace_hash"][:16] + "…",
            }
        )

    # Print markdown table
    headers = ["method", "converged", "steps", "final_state", "records", "trace_hash"]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        print("| " + " | ".join(row[h] for h in headers) + " |")


if __name__ == "__main__":
    main()
