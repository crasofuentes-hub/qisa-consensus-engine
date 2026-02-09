from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from qisa.perspectives import Opinion


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    initial_state: Mapping[str, Any]
    key: str = "x_target"
    state_field: str = "x"
    proposal_field: str = "x_target"


def perspectives():
    def p_fast(state, step):
        return Opinion("p_fast", {"x_target": 2}, 0.70, "Fast")

    def p_safe(state, step):
        return Opinion("p_safe", {"x_target": 0}, 0.60, "Safe")

    def p_bold(state, step):
        return Opinion("p_bold", {"x_target": 3}, 0.65, "Bold")

    p_fast.perspective_id = "p_fast"
    p_safe.perspective_id = "p_safe"
    p_bold.perspective_id = "p_bold"
    return [p_fast, p_safe, p_bold]


SCENARIO = Scenario(
    name="numeric_target_v1",
    initial_state={"x": 1},
)
