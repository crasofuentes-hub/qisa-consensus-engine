![CI](https://github.com/crasofuentes-hub/qisa-consensus-engine/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/crasofuentes-hub/qisa-consensus-engine?include_prereleases=false)

# QISA Consensus Engine

Deterministic, auditable **multi-perspective consensus** with explicit **fixpoint semantics** and **tamper-evident trace hashing**.

This repository provides a reference-grade core for building decision systems where **reproducibility** and **auditability** are first-class constraints.

## Key properties
- **Deterministic convergence**: fixpoint iteration converges (or fails fast) under bounded steps.
- **Idempotence**: re-running from a converged state returns the same final state and trace hash.
- **Tamper-evident traces**: hash chain per step enables verification of recorded executions.
- **Reproducible benchmarks**: pinned JSON result artifact + generated comparison table.

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Quickstart
Run the minimal example:
```bash
python examples/simple_decision.py
```

## Audit demo (trace export + verification)
This demo emits a JSON trace and verifies it end-to-end:
```bash
python examples/audit_demo.py
```

## Benchmarks (reproducible + pinned)
Generate benchmark output:
```bash
python -m bench.run_bench > bench/results_scenario_v1.json
```

Generate the comparison table:
```bash
python -m bench.make_results_table
```

## What QISA is / is not
**Is:** deterministic consensus engine + audit trace machinery (designed to sit under LLM or non-LLM perspectives).

**Is not:**
- an LLM
- stochastic sampling
- dependent on external services

## Repository layout
```text
src/qisa/          core engine (fixpoint, operators, traces)
bench/             benchmark harness + baselines
examples/          runnable demos
docs/              architecture, theory, verification notes
tests/             convergence/idempotence/trace/bench coverage
```

## Development
```bash
python -m ruff check .
python -m ruff format .
python -m pytest
```

## Citation
If you use this work, please cite via `CITATION.cff`.

## License
MIT (see `LICENSE`).

## Roadmap
- Add additional benchmark scenarios (non-numeric, adversarial disagreement, constrained consensus).
- Extend trace schema for richer provenance (inputs, operator params, perspective metadata).
- Add formal verification notes and/or proofs for key invariants (soundness of trace verification).
