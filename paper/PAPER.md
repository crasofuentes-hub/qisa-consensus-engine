# QISA Consensus Engine: Deterministic, Auditable Multi-Perspective Consensus with Fixpoint Semantics

**Author:** Oscar Fuentes Fernández

## Abstract
We present QISA Consensus Engine, a deterministic multi-perspective consensus core designed for auditability and reproducibility. The system models consensus as a bounded fixpoint process over an explicit state, producing a tamper-evident trace via stepwise hash chaining. QISA is not an LLM and does not depend on external services. It is intended as a verifiable substrate under either LLM-based or non-LLM “perspectives”, enabling transparent decision aggregation with reproducible benchmarks.

## Contributions
1. **Deterministic fixpoint engine** with bounded convergence and explicit idempotence expectations.
2. **Tamper-evident trace chain** enabling offline verification of recorded executions.
3. **Trace export + verification** utilities for audit workflows.
4. **Reproducible benchmark harness** with pinned JSON results and generated comparison tables.

## Problem statement
Multi-agent and multi-perspective decision systems are often difficult to audit because stochasticity and hidden state changes prevent exact reproduction. QISA targets the subset of systems where deterministic replay, trace verification, and artifact-based benchmarking are non-negotiable requirements.

## Method overview
- A consensus run iteratively applies a deterministic operator to a structured state.
- Each step produces a record containing state hash, decision hash, and a chained step hash.
- The run converges when the operator output is a fixpoint (or stops at max steps).
- A verifier recomputes the hash chain to detect tampering or mismatched execution.

## Claims and verification mapping
Each claim below is backed by a concrete repository artifact:

### C1 — Deterministic convergence (bounded)
- Evidence: `tests/test_convergence.py`
- Meaning: for the provided scenarios/operators, runs converge within configured max steps.

### C2 — Idempotence at fixpoint
- Evidence: `tests/test_idempotence.py`
- Meaning: once converged, re-running yields identical final state and trace hash.

### C3 — Tamper-evident trace hashing
- Evidence: `tests/test_trace_hash.py` and trace chain implementation in `src/qisa/traces.py`
- Meaning: altering any step breaks verification via chained hashes.

### C4 — Trace verification correctness (recompute and validate)
- Evidence: `tests/test_trace_verify.py` and verifier in `src/qisa/traces.py`
- Meaning: verifier accepts authentic traces and rejects tampered ones.

### C5 — Reproducible benchmark artifact schema
- Evidence: `bench/results_scenario_v1.json` and `tests/test_bench_artifact.py`
- Meaning: pinned results exist, are parseable, and match expected schema/keys.

## Reproducibility
Run benchmarks and generate comparisons:

```bash
python -m bench.run_bench > bench/results_scenario_v1.json
python -m bench.make_results_table
```

## Limitations
- QISA does not attempt to model natural-language reasoning; it provides deterministic consensus mechanics.
- Guarantees hold for deterministic operators and scenarios included in this repository.

## License
MIT.

