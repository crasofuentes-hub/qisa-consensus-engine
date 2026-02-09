# Quality Bar (Definition of Done)

This document defines what “reference-grade” means for this repository.
If all items below are satisfied, the project is considered **complete at the current scope** (not infinite).

## A. Engineering gates (must always be green)
- [ ] CI passes on Windows + Linux for Python 3.11 and 3.12.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m ruff format .` produces no changes after formatting.
- [ ] `python -m pytest` passes locally and in CI.

## B. Determinism & fixpoint guarantees (scope-limited to included scenarios/operators)
- [ ] Convergence tests exist and pass (bounded fixpoint iteration).
- [ ] Idempotence tests exist and pass (re-run at fixpoint yields same output and trace hash).

## C. Auditability guarantees
- [ ] Trace export exists and is usable (JSON serialization).
- [ ] Trace verification exists and detects tampering (hash chain recomputation).
- [ ] Tests cover trace hashing and trace verification.

## D. Reproducibility artifacts
- [ ] Pinned benchmark artifact exists: `bench/results_scenario_v1.json`.
- [ ] A test validates the pinned artifact schema keys.
- [ ] Comparison table is generated from artifacts (not hand-written claims).

## E. Documentation minimum (reference-grade)
- [ ] README contains install, quickstart, audit demo, and benchmarks.
- [ ] `docs/reproducibility.md` exists (auditor-grade steps).
- [ ] `docs/comparisons.md` exists (baselines, metrics, failure cases, structural differences).
- [ ] `paper/PAPER.md` exists and maps claims to verification artifacts.
- [ ] `CHANGELOG.md` exists and tracks releases.

## F. Release hygiene
- [ ] A Git tag exists for the reference release (`v0.1.0`).
- [ ] GitHub Release exists with notes (`RELEASE_NOTES_v0.1.0.md`).

## What is explicitly out of scope (so it does not become infinite)
- LLM model training or evaluation
- Probabilistic / stochastic consensus methods
- External service dependencies
- Proving properties for all possible operators (only the operators/scenarios shipped here)

## Upgrade policy
Future work should be added via new versions and must not weaken items A–F.

