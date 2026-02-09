# Reproducibility (Auditor-Grade)

This repository is designed so that a third party can reproduce and verify:
- deterministic consensus execution,
- tamper-evident trace integrity, and
- benchmark artifacts and comparison outputs.

## 1) Environment
Supported:
- Python 3.11+ (CI runs 3.11 and 3.12)
- Windows and Linux

## 2) Install (editable + dev)
From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## 3) Determinism gates (must pass)
Run the full quality gate:

```bash
python -m ruff check .
python -m ruff format .
python -m pytest
```

Expected:
- all tests pass (convergence, idempotence, trace hashing, trace verification, benchmark artifact schema)

## 4) Audit demo (trace export + verification)
Run:

```bash
python examples/audit_demo.py
```

Expected:
- JSON trace printed to stdout
- verification succeeds (no tampering detected)

## 5) Benchmarks (pinned artifact)
This repo includes a pinned benchmark artifact:
- `bench/results_scenario_v1.json`

It is validated by:
- `tests/test_bench_artifact.py`

Optional regeneration (should reproduce the same schema and be consistent with deterministic behavior):

```bash
python -m bench.run_bench > bench/results_scenario_v1.json
```

Note:
- When regenerating on Windows, ensure the output is UTF-8 **without BOM**.

## 6) Comparison table (generated from artifacts)
Generate:

```bash
python -m bench.make_results_table
```

Expected:
- a Markdown table printed to stdout with method rows and trace hashes

## 7) What counts as “reproduced”
A run is considered reproduced when:
- `python -m pytest` passes, and
- trace verification passes on an exported trace, and
- pinned artifact exists and matches expected schema keys.

