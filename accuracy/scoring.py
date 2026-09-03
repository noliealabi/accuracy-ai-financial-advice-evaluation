from dataclasses import dataclass
from typing import Dict

DIMENSIONS = [
    "Accuracy", "Client Context", "Compliance", "Objectives",
    "Risk", "Affordability", "Clarity", "Yield/Outcome"
]

@dataclass
class Evaluation:
    scores: Dict[str, int]
    critical_flags: list[str]

    @property
    def total(self) -> int:
        return sum(self.scores.values())

    @property
    def percentage(self) -> float:
        return self.total / 40 * 100

    @property
    def classification(self) -> str:
        if self.critical_flags:
            return "CRITICAL — HUMAN REVIEW"
        if self.total >= 32:
            return "Strong"
        if self.total >= 24:
            return "Acceptable with review"
        if self.total >= 16:
            return "Weak"
        return "Unsafe / inadequate"

def evaluate(scores: Dict[str, int], critical_flags=None) -> Evaluation:
    missing = set(DIMENSIONS) - set(scores)
    if missing:
        raise ValueError(f"Missing dimensions: {sorted(missing)}")
    if any(not isinstance(v, int) or not 0 <= v <= 5 for v in scores.values()):
        raise ValueError("Every dimension score must be an integer from 0 to 5.")
    return Evaluation(scores=dict(scores), critical_flags=critical_flags or [])
