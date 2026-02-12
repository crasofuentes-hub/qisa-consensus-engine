# QISA Tools (Trace Export + External Verification)

This folder contains portable, reproducible utilities for exporting a QISA run trace to JSON and verifying that trace externally (without calling the consensus engine logic).

Core goals:
- Reproducibility: same inputs -> same hashes
- Auditability: chained step hashes
- Portability: run on host or inside Docker
- Non-invasive verification: validate JSON trace without touching engine internals

## What’s included

- export_trace_demo.py
  - Writes: tools/_artifacts/trace_demo.json

- verify_trace_json.py
  - Validates:
    - per-step hash chain correctness
    - trace_hash matches last step_hash
  - Prints: VALID / INVALID (non-zero exit on failure)

## Host usage (Windows PowerShell 5.1)

From repo root:

powershell:
  Set-StrictMode -Version Latest
  $ErrorActionPreference = "Stop"
  Set-Location C:\repos\qisa-consensus-engine
  python tools\export_trace_demo.py
  python tools\verify_trace_json.py tools\_artifacts\trace_demo.json

Expected:
- Export: WROTE: tools/_artifacts/trace_demo.json
- Verify: VALID

## Docker usage

Build:
  docker build --no-cache -t qisa-consensus-engine:dev .

Export (bind mount so artifacts land on host):
  docker run --rm -v ${PWD}:/app qisa-consensus-engine:dev python tools/export_trace_demo.py

Verify:
  docker run --rm -v ${PWD}:/app qisa-consensus-engine:dev python tools/verify_trace_json.py tools/_artifacts/trace_demo.json

## Trace schema v1 (minimal)

Top-level keys:
- run_id (string)
- input_hash (string)
- output_hash (string)
- trace_hash (string)
- records (array)

Record keys:
- step (int)
- state (object)
- decision (object)
- state_hash (string)
- decision_hash (string)
- prev_step_hash (string)
- step_hash (string)

Verification rule:
- Recompute each step_hash from (step, state_hash, decision_hash, prev_step_hash)
- Chain must match
- trace_hash must equal last step_hash
