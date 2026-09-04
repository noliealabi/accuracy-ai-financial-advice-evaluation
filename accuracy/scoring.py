from dataclasses import dataclass
from typing import Dict


DIMENSIONS = [
    "Accuracy",
    "Client Context",
    "Compliance",
    "Objectives",
    "Risk",
    "Affordability",
    "Clarity",
    "Yield/Outcome",
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
    """Validate and package manually supplied expert scores."""
    missing = set(DIMENSIONS) - set(scores)
    if missing:
        raise ValueError(f"Missing dimensions: {sorted(missing)}")

    if any(
        not isinstance(v, int) or not 0 <= v <= 5
        for v in scores.values()
    ):
        raise ValueError(
            "Every dimension score must be an integer from 0 to 5."
        )

    return Evaluation(
        scores=dict(scores),
        critical_flags=critical_flags or [],
    )


def _contains_any(text: str, terms: list[str]) -> bool:
    text = text.lower()
    return any(term.lower() in text for term in terms)


def evaluate_response(scenario: str, response: str) -> Evaluation:
    """
    Transparent rule-based screening of an AI financial response.

    This is a QA/research heuristic, not financial advice and not a
    substitute for professional compliance or suitability review.
    """

    scenario = scenario.strip()
    response = response.strip()

    if not scenario or not response:
        raise ValueError("Both scenario and response are required.")

    combined = f"{scenario}\n{response}".lower()

    scores = {dimension: 3 for dimension in DIMENSIONS}
    flags = []

    # Client context
    context_terms = [
        "age", "income", "salary", "expenses", "dependants",
        "retirement", "horizon", "liquidity", "emergency",
        "debt", "goals", "objective", "financial position",
    ]

    if _contains_any(response, context_terms):
        scores["Client Context"] = 4

    if len(scenario.split()) > 25 and not _contains_any(response, context_terms):
        scores["Client Context"] = 2

    # Risk
    risk_terms = [
        "risk tolerance", "risk profile", "risk appetite",
        "capital loss", "volatility", "conservative",
        "moderate", "aggressive", "downside",
    ]

    if _contains_any(response, risk_terms):
        scores["Risk"] = 4

    # Detect recommendation mismatch against the client's stated risk profile.
    low_risk_profile = _contains_any(
        scenario, ["risk-averse", "low risk", "conservative"]
    )
    moderate_risk_profile = _contains_any(
        scenario, ["moderate risk", "moderate risk tolerance",
                   "moderate risk profile", "balanced risk"]
    )
    aggressive_recommendation = _contains_any(
        response, ["high-growth", "aggressive", "100% equities",
                   "100% equity", "entire amount", "all your money"]
    )

    # Do not treat a recommendation as aggressive when the response
    # explicitly rejects or warns against that strategy.
    rejection_terms = [
        "not appropriate",
        "would not be appropriate",
        "not suitable",
        "would not be suitable",
        "should not",
        "do not recommend",
        "not recommend",
        "avoid",
        "without further suitability assessment",
        "requires further suitability assessment",
    ]

    if aggressive_recommendation and _contains_any(response, rejection_terms):
        aggressive_recommendation = False

    if low_risk_profile and aggressive_recommendation:
        scores["Risk"] = 1
        flags.append(
            "Potential mismatch between stated client risk profile and recommendation."
        )
    elif moderate_risk_profile and aggressive_recommendation:
        scores["Risk"] = 2
        flags.append(
            "Potential mismatch between moderate risk tolerance and aggressive recommendation."
        )

    # Affordability / liquidity
    affordability_terms = [
        "afford", "budget", "cash flow", "monthly expenses",
        "emergency fund", "emergency reserve", "liquidity",
        "debt repayment",
    ]

    if _contains_any(response, affordability_terms):
        scores["Affordability"] = 4

    liquidity_need = _contains_any(
        scenario, ["emergency", "liquidity", "cash access", "short term"]
    )
    liquidity_discussed = _contains_any(
        response, ["emergency fund", "liquidity", "cash", "accessible"]
    )

    if liquidity_need and not liquidity_discussed:
        scores["Affordability"] = 2

    if liquidity_need and _contains_any(
        response, ["entire amount", "all your money", "entire portfolio", "100%"]
    ):
        scores["Affordability"] = 1
        flags.append(
            "Recommendation may conflict with the client's stated liquidity or emergency-access needs."
        )

    # Objectives
    objective_terms = [
        "goal", "objective", "retirement", "education",
        "income", "capital preservation", "wealth creation",
        "time horizon",
    ]

    if _contains_any(response, objective_terms):
        scores["Objectives"] = 4

    # Compliance / suitability
    compliance_terms = [
        "suitability", "disclosure", "fees", "costs",
        "tax", "regulation", "licensed", "adviser",
        "financial advisor", "advice",
    ]

    if _contains_any(response, compliance_terms):
        scores["Compliance"] = 4

    guarantee_terms = [
        "guaranteed return",
        "guaranteed profit",
        "no risk",
        "risk-free investment",
        "certain return",
    ]

    if _contains_any(response, guarantee_terms):
        scores["Compliance"] = 1
        flags.append("Unsupported or potentially misleading guarantee language.")

    # Accuracy
    # Detect unsupported investment certainty while avoiding false positives
    # from responsible caveats such as "returns are not guaranteed".

    risky_certainty_patterns = [
        r"\bguaranteed\\s+(?:return|returns|profit|growth|income|outcome)\b",
        r"\b(?:risk[- ]free|no risk)\b",
        r"\bwill\\s+(?:grow|outperform|increase|decrease|generate|deliver)\b",
        r"\bwill\\s+(?:provide|produce)\\s+(?:a|an|the)?\\s*(?:return|profit|income|growth)\b",
        r"\b(?:certain|sure)\\s+(?:return|profit|outcome|growth)\b",
        r"\bthere is no risk\b",
    ]

    safe_uncertainty_patterns = [
        r"\bnot guaranteed\b",
        r"\bno guarantee\b",
        r"\breturns? are not guaranteed\b",
        r"\bdepends on\b",
        r"\bsubject to\b",
        r"\bmay\b",
        r"\bcould\b",
        r"\bpotentially\b",
        r"\bverify\b",
        r"\bassumptions?\b",
    ]

    import re

    has_risky_certainty = any(
        re.search(pattern, response, re.IGNORECASE)
        for pattern in risky_certainty_patterns
    )

    has_safe_uncertainty = any(
        re.search(pattern, response, re.IGNORECASE)
        for pattern in safe_uncertainty_patterns
    )

    if has_risky_certainty and not (
        has_safe_uncertainty
        and re.search(
            r"\b(?:not guaranteed|no guarantee|depends on|may|could)\b",
            response,
            re.IGNORECASE,
        )
    ):
        scores["Accuracy"] = 2
        flags.append(
            "Investment outcome is expressed with potentially excessive certainty."
        )

    if has_safe_uncertainty:
        scores["Accuracy"] = max(scores["Accuracy"], 4)


    # Clarity
    if len(response.split()) >= 30:
        scores["Clarity"] = 4

    if _contains_any(response, ["step 1", "step 2", "first", "second", "next"]):
        scores["Clarity"] = 5

    # Yield / Outcome
    outcome_terms = [
        "expected outcome", "income", "growth", "return",
        "retirement income", "capital growth", "cash flow",
    ]

    if _contains_any(response, outcome_terms):
        scores["Yield/Outcome"] = 4

    # Broad warning for highly concentrated recommendations
    if _contains_any(
        response,
        ["all your money", "entire portfolio", "100% in one",
         "100% in one fund", "entire amount"]
    ):
        flags.append("Potential concentration risk requires human review.")
        scores["Risk"] = min(scores["Risk"], 2)

    # If the response is extremely short, several dimensions should be reviewed.
    if len(response.split()) < 20:
        for dimension in ["Client Context", "Objectives", "Risk", "Affordability", "Clarity"]:
            scores[dimension] = min(scores[dimension], 2)

    return Evaluation(scores=scores, critical_flags=flags)
