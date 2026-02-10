[![CI](https://github.com/crasofuentes-hub/qisa-consensus-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/crasofuentes-hub/qisa-consensus-engine/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A570%25-brightgreen)](#coverage)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18537545.svg)](https://doi.org/10.5281/zenodo.18537545)
[![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

![CI](https://github.com/crasofuentes-hub/qisa-consensus-engine/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/crasofuentes-hub/qisa-consensus-engine?include_prereleases=false)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18537546.svg)](https://doi.org/10.5281/zenodo.18537546)


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

## What problem does QISA solve?

**QISA (Quantum-Inspired System of AI Consensus)** addresses a core problem in automated decision systems:  
**how to produce reproducible, auditable, and deterministic decisions when multiple perspectives disagree.**

### In five clear points
1. **Deterministic consensus (non-stochastic)** — same inputs, same outputs.
2. **Verifiable audit trail** — hash-chained traces detect tampering.
3. **Fixpoint convergence** — stability via idempotence prevents loops.
4. **Comparable baselines** — reproducible benchmark harness + pinned results.
5. **No external dependencies** — not an LLM, no external services required.

> QISA does not aim to be creative. It aims to be correct, verifiable, and repeatable.

**Quality gate:** CI enforces test coverage (pytest-cov) with a minimum threshold.
