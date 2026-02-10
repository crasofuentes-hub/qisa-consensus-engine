[![CI](https://github.com/crasofuentes-hub/qisa-consensus-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/crasofuentes-hub/qisa-consensus-engine/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A570%25-brightgreen)](#coverage)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18537546.svg)](https://doi.org/10.5281/zenodo.18537546)
[![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

# QISA Consensus Engine

**Deterministic, auditable multi-perspective consensus** with explicit **fixpoint semantics** and **tamper-evident trace hashing**.

QISA provides a **reference-grade core** for decision systems where **reproducibility, auditability, and determinism** are first-class constraints.

This repository intentionally avoids stochasticity and external services in order to support **verifiable execution** and **post-hoc inspection**.

---

## Key properties

- **Deterministic convergence**  
  Fixpoint iteration converges (or fails fast) under bounded steps.

- **Idempotence**  
  Re-running from a converged state yields the same final state and trace hash.

- **Tamper-evident traces**  
  Each execution step is hash-chained; any post-hoc mutation is detectable.

- **Reproducible benchmarks**  
  Benchmarks emit pinned JSON artifacts plus a generated comparison table.



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
---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
