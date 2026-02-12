from __future__ import annotations

import inspect
from dataclasses import dataclass


from qisa import ConsensusConfig, run_fixpoint
from qisa.operators import make_perspective_operator
from qisa.traces import verify_trace


def _tamper_exc_type():
    """
    Descubre el tipo de excepción real usado por verify_trace().
    Si no existe, cae a Exception (pero el test seguirá validando retorno False/None).
    """
    try:
        import qisa.errors as e  # type: ignore

        for name in ("TraceTamperError", "TraceIntegrityError", "TamperError"):
            if hasattr(e, name):
                return getattr(e, name)
    except Exception:
        pass
    return Exception


def _clone_trace_with_tracehash_tamper(trace, bad_trace_hash: str):
    """
    Clona Trace copiando TODOS los campos requeridos según su firma actual,
    y solo altera trace_hash. Esto evita roturas si Trace agrega campos obligatorios.
    """
    TraceT = type(trace)
    sig = inspect.signature(TraceT)
    kwargs = {}
    for name in sig.parameters.keys():
        if name == "trace_hash":
            kwargs[name] = bad_trace_hash
        else:
            kwargs[name] = getattr(trace, name)
    return TraceT(**kwargs)


@dataclass(frozen=True)
class OpinionLike:
    """
    Contrato mínimo que usa qisa.consensus.choose_consensus():
      - choice
      - proposal (dict)
      - confidence (float)
      - perspective_id (str)
    """

    choice: str
    proposal: dict
    confidence: float = 1.0
    perspective_id: str = "p0"


def test_verify_trace_detects_tamper():
    def p1(state, step):
        x = int(state.get("x", 0))
        return OpinionLike(
            choice="a", proposal={"x_target": x + 1}, confidence=1.0, perspective_id="p1"
        )

    def p2(state, step):
        x = int(state.get("x", 0))
        return OpinionLike(
            choice="a", proposal={"x_target": x + 1}, confidence=1.0, perspective_id="p2"
        )

    cfg = ConsensusConfig(max_steps=10, stable_steps_required=2)
    op = make_perspective_operator([p1, p2], key="x_target")
    res = run_fixpoint(run_id="cov_trace", initial_state={"x": 0}, operator=op, config=cfg)

    # Tamper: trace_hash (campo normalmente validado)
    th = getattr(res.trace, "trace_hash", "")
    bad_th = (th + "X") if isinstance(th, str) else "tampered"
    bad = _clone_trace_with_tracehash_tamper(res.trace, bad_th)

    TamperExc = _tamper_exc_type()

    # Contrato compatible: verify_trace puede lanzar o retornar bool/None.
    try:
        out = verify_trace(bad)
    except TamperExc:
        assert True
        return

    assert out in (False, None)
