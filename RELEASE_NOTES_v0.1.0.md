# QISA Consensus Engine — v0.1.0

## Scope
First reference release of a **deterministic, auditable consensus engine*** with explicit fixpoint semantics.

## Core guarantees
- Deterministic convergence (fixpoint + idempotence)
- Tamper-evident trace hashing (hash chain per step)
- Verifiable trace export and verification
- Reproducible benchmark harness with pinned results

## What is included
- Multi-perspective opinions + deterministic consensus operator
- Trace export (`trace_to_json`) and verification (`verify_trace`)
- Benchmark harness (`bench.run_bench`) with baselines
- Auto-generated comparison table from pinned JSON results
- Tests covering convergence, idempotence, tamper-evidence, and benchmarks

## What this is NOT
- Not an LLM
- Not stochastic
- Not dependent on external services

## Reproducibility

```bash
python -m bench.run_bench > bench/results_scenario_v1.json
python -m bench.make_results_table
```


## Status
Reference-grade core suitable for audited decision systems and for integration under LLL or non-LLM perspectives.
