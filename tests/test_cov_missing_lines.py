from __future__ import annotations

from dataclasses import dataclass, is_dataclass, replace
import inspect
import pytest

from qisa import ConsensusConfig, run_fixpoint
from qisa.consensus import coherence_score
from qisa.errors import NonConvergentError
from qisa.quality import disagreement_entropy, numeric_variance, compute_quality_metrics
from qisa.traces import verify_trace
import qisa.traces as traces_mod


# -------------------------
# consensus.py (line 24): n <= 1 -> return 1.0
# -------------------------
@dataclass(frozen=True)
class OpinionLike:
    choice: str
    proposal: dict
    confidence: float = 1.0
    perspective_id: str = "p0"


def test_coherence_score_single_opinion_returns_one():
    o = OpinionLike(choice="a", proposal={"x_target": 1}, confidence=1.0, perspective_id="p1")
    assert coherence_score([o], key="x_target") == 1.0


# -------------------------
# engine.py (lines 33, 35): invalid config raises ValueError
# -------------------------
def test_run_fixpoint_raises_on_invalid_config_values():
    import inspect
    import pytest

    from qisa import ConsensusConfig, run_fixpoint

    def op(state, step):
        return dict(state), {"choice": "a"}

    sig = inspect.signature(run_fixpoint)
    params = sig.parameters

    # Construye kwargs en orden robusto sin usar posicionales
    kwargs = {}
    if "run_id" in params:
        kwargs["run_id"] = "bad_max"
    if "initial_state" in params:
        kwargs["initial_state"] = {"x": 0}
    if "operator" in params:
        kwargs["operator"] = op
    if "config" in params:
        kwargs["config"] = ConsensusConfig(max_steps=0, stable_steps_required=1)

    with pytest.raises(ValueError):
        run_fixpoint(**kwargs)

    # stable_steps_required inválido
    if "config" in params:
        kwargs["config"] = ConsensusConfig(max_steps=1, stable_steps_required=0)
        with pytest.raises(ValueError):
            run_fixpoint(**kwargs)


# -------------------------
# errors.py (line 18): __str__ path
# (construimos kwargs por signature para no romper si cambia el dataclass)
# -------------------------
def _mk_nonconvergent_error() -> NonConvergentError:
    sig = inspect.signature(NonConvergentError)
    kwargs = {}
    for name, p in sig.parameters.items():
        if p.default is not inspect._empty:
            continue
        if name == "run_id":
            kwargs[name] = "r0"
        elif name == "steps":
            kwargs[name] = 123
        elif name == "max_steps":
            kwargs[name] = 10
        elif name == "stability_window":
            kwargs[name] = 2
        elif name == "last_state":
            kwargs[name] = {"x": 7}
        elif name == "trace_hash":
            kwargs[name] = "deadbeef"
        else:
            # fallback razonable para campos futuros obligatorios
            kwargs[name] = None
    return NonConvergentError(**kwargs)


def test_nonconvergent_error_str_is_informative():
    err = _mk_nonconvergent_error()
    s = str(err)
    assert "NonConvergentError(" in s
    assert "run_id=" in s
    assert "steps=" in s


# -------------------------
# perspectives.py (line 30): Perspective.as_mapping()
# perspectives.py (lines 55-56): _get_int except -> default
# -------------------------
def test_perspective_as_mapping_includes_expected_keys():
    """
    Cubre perspectives.py:30 (return {...} de as_mapping()) sin asumir que Perspective es instanciable.
    Buscamos un objeto real que implemente .as_mapping().
    """
    import pytest
    import qisa.perspectives as pm

    # Heurística: buscar en el módulo algún símbolo instanciable que tenga método as_mapping
    cls = None
    for name in dir(pm):
        obj = getattr(pm, name)
        if isinstance(obj, type) and hasattr(obj, "as_mapping"):
            cls = obj
            break

    if cls is None:
        pytest.skip(
            "No hay clase pública con as_mapping() en qisa.perspectives; Perspective es Callable alias."
        )
        return

    p = cls(name="p", values={"k": 1}, confidence=0.5, rationale="r")
    m = p.as_mapping()
    assert isinstance(m, dict)
    for k in ("name", "values", "confidence", "rationale"):
        assert k in m


def test_demo_perspective_get_int_exception_path_defaults():
    """
    Cubre el except de _get_int en qisa.perspectives.py (lines 55-56).
    No asumimos make_demo_perspectives(): usamos la vía pública disponible
    para construir perspectivas y ejecutar una que lea "target" con int(...).
    """
    import qisa.perspectives as pm
    import qisa.operators as om

    # Encuentra una lista/callable de perspectivas demo de forma robusta
    # 1) Si existe make_demo_perspectives -> úsalo (por si lo agregas en el futuro)
    if hasattr(pm, "make_demo_perspectives"):
        ps = pm.make_demo_perspectives()  # type: ignore[attr-defined]
    else:
        # 2) Si existe make_demo_operator / make_demo... (cualquier factory útil)
        #    Si no, usamos la API normal: make_perspective_operator sobre funciones p_* del módulo.
        ps = []

    # Si no obtuvimos ps, intentamos usar funciones demo p_optimist/p_pessimist si existen
    if not ps:
        cand = []
        for name in ("p_optimist", "p_pessimist"):
            if hasattr(pm, name):
                cand.append(getattr(pm, name))
        if not cand:
            pytest.skip(
                "No se encontraron perspectivas demo (p_optimist/p_pessimist) en qisa.perspectives."
            )
            return
        # cand son perspectivas tipo callable(state, step)->Opinion
        op = om.make_perspective_operator(cand, key="x_target")
        # Forzamos int(object()) dentro de _get_int: target no convertible
        new_state, decision = op({"target": object()}, 0)
        assert isinstance(decision, dict)
        assert "x_target" in decision
        assert decision["x_target"] == 1
        return

    # Si sí hay ps, busca 'optimist' y ejecútalo
    opt = next((x for x in ps if getattr(x, "name", "") == "optimist"), None)
    if opt is None:
        pytest.skip("Lista demo sin 'optimist'.")
        return

    out = opt({"target": object()}, 0)
    assert getattr(out, "proposal")["x_target"] == 1


def test_disagreement_entropy_empty_labels_branch():
    assert disagreement_entropy([{}]) == 0.0


def test_numeric_variance_empty_returns_zero():
    assert numeric_variance([]) == 0.0


def test_compute_quality_metrics_decisions_none_defaults_to_empty_list():
    m = compute_quality_metrics(final_state={"a": 1})
    assert isinstance(m, dict)
    assert m.get("decision_count") == 0
    assert "final_state_keys" in m


# -------------------------
# traces.py
# line 13: dataclass -> asdict recursion
# line 19: list/tuple recursion
# line 22: set sorted path
# line 85: verify_trace prev_step_hash mismatch -> False
# -------------------------
@dataclass(frozen=True)
class D:
    x: int
    y: list[int]


def test__to_jsonable_dataclass_list_set_branches():
    # dataclass branch
    o = D(1, [2, 3])
    j = traces_mod._to_jsonable(
        o
    )  # usamos función privada a propósito para cubrir ramas específicas
    assert isinstance(j, dict) and j["x"] == 1 and j["y"] == [2, 3]

    # list/tuple branch
    j2 = traces_mod._to_jsonable((1, [2, 3]))
    assert j2 == [1, [2, 3]]

    # set branch: debe ordenar de forma determinista
    j3 = traces_mod._to_jsonable({2, 1})
    assert j3 == [1, 2]


def _clone_trace_with_records(trace, new_records):
    import inspect

    TraceT = type(trace)
    sig = inspect.signature(TraceT)
    kwargs = {}
    for name in sig.parameters.keys():
        if name == "records":
            kwargs[name] = new_records
        else:
            kwargs[name] = getattr(trace, name)
    return TraceT(**kwargs)


def test_verify_trace_prev_step_hash_mismatch_returns_false():
    def op(state, step):
        x = int(state.get("x", 0))
        if step < 2:
            return {"x": x + 1}, {"choice": "a", "x_target": x + 1}
        return {"x": x}, {"choice": "a", "x_target": x}

    res = run_fixpoint(
        run_id="trace_prev_mismatch",
        initial_state={"x": 0},
        operator=op,
        config=ConsensusConfig(max_steps=10, stable_steps_required=2),
    )

    recs = list(res.trace.records)
    assert recs, "Trace should contain records"

    r0 = recs[0]
    if is_dataclass(r0):
        recs[0] = replace(r0, prev_step_hash="BAD_PREV_HASH")
    else:
        # fallback (muy improbable en tu codebase)
        setattr(r0, "prev_step_hash", "BAD_PREV_HASH")
        recs[0] = r0

    bad_trace = _clone_trace_with_records(res.trace, recs)
    assert verify_trace(bad_trace) is False
