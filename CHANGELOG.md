# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and the project follows Semantic Versioning (major.minor.patch) as an operational convention.

## [0.1.0] - 2026-02-08
### Added
- Deterministic fixpoint engine with convergence and idempotence tests.
- Tamper-evident trace hash chain with offline verification.
- Trace export (`trace_to_json`) and verification (`verify_trace`).
- Multi-perspective opinions and deterministic consensus operator.
- Reproducible benchmark harness with baselines and pinned results artifact.
- Auto-generated comparisons table from pinned benchmark JSON.
- CI for Windows/Linux and Python 3.11/3.12, plus Ruff formatting/linting.
- Reference paper mapping claims to repository verification artifacts.

### Notes
- Release tag: `v0.1.0`

## [0.1.1] - Unreleased
### Planned
- Additional benchmark scenarios (adversarial disagreement / oscillation guards).
- Expanded comparison metrics (distance-to-target, disagreement magnitude).
- Stronger formal verification notes for trace soundness invariants.

