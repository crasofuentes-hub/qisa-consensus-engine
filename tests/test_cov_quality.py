from qisa.quality import compute_quality_metrics, disagreement_entropy


def test_quality_branches():
    # disagreement_entropy: no Mapping y sin "choice"
    h = disagreement_entropy([{"k": "v"}, {"k": "v2"}, "raw"])
    assert h >= 0.0

    # compute_quality_metrics: sin args -> {}
    assert compute_quality_metrics() == {}

    # decisions con x_target no convertible + final_state
    m = compute_quality_metrics(
        decisions=[{"x_target": "nope", "choice": "a"}, {"x_target": 1.0}],
        final_state={"z": 1, "a": 2},
    )
    assert isinstance(m, dict)
    assert "final_state_keys" in m
    assert m["decision_count"] == 2
