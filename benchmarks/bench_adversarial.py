from __future__ import annotations

import csv
import time
import tracemalloc
from pathlib import Path
from typing import Any, Mapping


def _load_export_demo_module() -> Any:
    demo_path = Path(__file__).resolve().parents[1] / "tools" / "export_trace_demo.py"
    if not demo_path.exists():
        raise FileNotFoundError(f"Missing: {demo_path}")

    import importlib.util  # noqa: PLC0415

    spec = importlib.util.spec_from_file_location("_qisa_export_trace_demo", demo_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to create import spec for export_trace_demo.py")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _trace_hash_from_result(res: Any) -> str:
    if hasattr(res, "trace_hash") and isinstance(res.trace_hash, str):
        return res.trace_hash
    if hasattr(res, "trace") and hasattr(res.trace, "trace_hash"):
        return str(res.trace.trace_hash)
    return ""


def _steps_from_result(res: Any) -> int | None:
    if hasattr(res, "steps") and isinstance(res.steps, int):
        return res.steps
    if hasattr(res, "trace") and hasattr(res.trace, "records"):
        try:
            return len(res.trace.records)
        except Exception:
            return None
    return None


def _stop_reason_from_result(res: Any) -> str:
    for k in ("stop_reason", "reason", "status"):
        if hasattr(res, k):
            v = getattr(res, k)
            if isinstance(v, str):
                return v
    return ""


def run_case(case_name: str) -> dict[str, Any]:
    # Importa QISA core
    from qisa.engine import run_fixpoint  # noqa: PLC0415
    import qisa.engine as eng  # noqa: PLC0415
    from qisa.types import ConsensusConfig  # noqa: PLC0415

    # Cargamos el demo que YA es estable (export/verify)
    demo = _load_export_demo_module()

    if not hasattr(demo, "op"):
        raise RuntimeError(
            "tools/export_trace_demo.py no expone 'op'. "
            f"Símbolos: {sorted([x for x in dir(demo) if not x.startswith('_')])}"
        )

    operator = getattr(demo, "op")

    # Initial state mínimo. (Si tu op requiere otras keys, el error saldrá explícito en 'error')
    initial_state: Mapping[str, Any] = {
        "case": case_name,
        "x": 0,
        "choice": "A",
        "toggle": False,
        "values": [1, 2, 3],
    }

    # Config adversarial (límite pequeño para detectar loops rápido)
    # Si tu ConsensusConfig no tiene max_steps, el error quedará reportado en CSV.
    cfg = ConsensusConfig(max_steps=64)

    status = "OK"
    ok = False
    steps: int | None = None
    stop_reason = ""
    trace_hash = ""
    error = ""

    t0 = time.perf_counter()
    tracemalloc.start()

    try:
        res = run_fixpoint(
            run_id=case_name, initial_state=initial_state, operator=operator, config=cfg
        )

        status = "OK"
        ok = True

        trace_hash = _trace_hash_from_result(res)
        steps = _steps_from_result(res)
        stop_reason = _stop_reason_from_result(res)

        if hasattr(res, "converged") and isinstance(res.converged, bool):
            ok = res.converged
        if hasattr(res, "ok") and isinstance(res.ok, bool):
            ok = res.ok

    except getattr(eng, "NonConvergentError", Exception) as e:
        status = "NONCONVERGED"
        ok = False
        error = f"{type(e).__name__}: {e}"
        if hasattr(e, "trace_hash"):
            trace_hash = str(getattr(e, "trace_hash"))

    except Exception as e:
        status = "ERROR"
        ok = False
        error = f"{type(e).__name__}: {e}"

    finally:
        dt_ms = (time.perf_counter() - t0) * 1000.0
        peak_kb = tracemalloc.get_traced_memory()[1] / 1024.0
        tracemalloc.stop()

    return {
        "case": case_name,
        "status": status,
        "ok": ok,
        "ms": round(dt_ms, 3),
        "peak_kb": int(peak_kb),
        "steps": steps if steps is not None else "",
        "stop_reason": stop_reason,
        "trace_hash": trace_hash,
        "error": error,
    }


def write_results(rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    out_dir = Path(__file__).resolve().parent / "_results"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "results.csv"
    md_path = out_dir / "results.md"

    cols = ["case", "status", "ok", "ms", "peak_kb", "steps", "stop_reason", "trace_hash", "error"]

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

    lines = []
    lines.append("| case | status | ok | ms | peak_kb | steps | stop_reason | trace_hash |")
    lines.append("|---|---|---:|---:|---:|---:|---|---|")
    for r in rows:
        lines.append(
            f"| {r['case']} | {r['status']} | {str(r['ok'])} | {r['ms']} | {r['peak_kb']} | {r['steps']} | {r['stop_reason']} | {r['trace_hash']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return csv_path, md_path


def main() -> int:
    cases = [
        "choice_conflict_3way",
        "deadlock_flipflop",
        "numeric_spread",
    ]

    rows: list[dict[str, Any]] = []
    for c in cases:
        try:
            rows.append(run_case(c))
        except Exception as e:
            # Nunca revienta el benchmark: reporta el error en el row
            rows.append(
                {
                    "case": c,
                    "status": "ERROR",
                    "ok": False,
                    "ms": 0,
                    "peak_kb": 0,
                    "steps": "",
                    "stop_reason": "",
                    "trace_hash": "",
                    "error": f"{type(e).__name__}: {e}",
                }
            )

    csv_path, md_path = write_results(rows)
    print(f"WROTE: {csv_path}")
    print(f"WROTE: {md_path}")

    # Si hay ERROR, devolvemos 2 para CI
    if any(r["status"] == "ERROR" for r in rows):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
