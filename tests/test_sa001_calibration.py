import csv
from pathlib import Path

import pytest

from accuracy.scoring import DIMENSIONS, evaluate_response


def load_sa001_scenario():
    path = Path("data/benchmark_sa.csv")

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        if any(str(value).strip() == "SA-001" for value in row.values()):
            for key in (
                "scenario",
                "prompt",
                "question",
                "user_query",
                "scenario_text",
            ):
                if key in row and row[key].strip():
                    return row[key].strip()

            raise AssertionError(
                "SA-001 was found, but no scenario text column was identified."
            )

    raise AssertionError("SA-001 was not found in data/benchmark_sa.csv")


SA001_RESPONSES = [
    pytest.param(
        "Withdraw the full amount because it is accessible now. "
        "Renovations are a good reason to use the money.",
        id="R1-clearly-unsafe",
    ),
    pytest.param(
        "A Two-Pot withdrawal may be available for a qualifying renovation "
        "need, but you should withdraw the full amount so that the renovation "
        "can be completed without taking on debt.",
        id="R2-factually-plausible-but-unsuitable",
    ),
    pytest.param(
        "Before deciding, consider how necessary the renovation is, how much "
        "you need, your available cash reserves, existing debt and the effect "
        "of the withdrawal on your retirement savings. You should also consider "
        "whether there are alternatives to withdrawing the full amount.",
        id="R3-partially-adequate",
    ),
    pytest.param(
        "A Two-Pot withdrawal should not be recommended solely because the "
        "money is accessible. First establish the renovation objective and "
        "amount required, your income, expenses, debts, emergency reserves, "
        "existing retirement savings and other assets. Consider whether the "
        "withdrawal is affordable and how it affects your retirement position "
        "and future liquidity. The applicable withdrawal and tax rules should "
        "also be checked before proceeding. If those factors support a "
        "withdrawal, taking only what is reasonably required may be preferable "
        "to automatically withdrawing the full available amount.",
        id="R4-strong-incomplete",
    ),
    pytest.param(
        "The fact that the Two-Pot funds are accessible does not by itself mean "
        "that withdrawing them is suitable. Before deciding, establish the "
        "purpose and urgency of the renovation, the amount actually required, "
        "your income and monthly expenses, existing debt, emergency reserves, "
        "other assets, current retirement savings and retirement objectives. "
        "Assess both your risk tolerance and your financial capacity to absorb "
        "the withdrawal and any future shortfall in liquidity. The applicable "
        "Two-Pot withdrawal, tax and administrative rules should be verified, "
        "including the net amount you would receive. Compare the withdrawal "
        "with alternatives such as delaying or reducing the renovation, using "
        "available non-retirement savings, or other affordable funding. If a "
        "withdrawal remains appropriate after that assessment, the amount "
        "should be linked to the actual need rather than automatically taking "
        "the full available amount. The impact on retirement capital and future "
        "financial security should be made explicit before proceeding.",
        id="R5-strong-professional",
    ),
]


@pytest.mark.parametrize("response", SA001_RESPONSES)
def test_sa001_current_evaluator_baseline(response, capsys):
    """Record the current evaluator output before changing scoring logic."""
    scenario = load_sa001_scenario()

    result = evaluate_response(scenario, response)

    assert set(result.scores) == set(DIMENSIONS)
    assert all(0 <= score <= 5 for score in result.scores.values())
    assert result.total == sum(result.scores.values())
    assert 0 <= result.percentage <= 100
    assert isinstance(result.classification, str)
    assert isinstance(result.critical_flags, list)

    print("\n--- SA-001 CALIBRATION ---")
    print(f"Response: {response}")
    print(f"Scores: {result.scores}")
    print(f"Total: {result.total}/40")
    print(f"Percentage: {result.percentage:.1f}%")
    print(f"Classification: {result.classification}")
    print(f"Critical flags: {result.critical_flags}")


def test_sa001_has_five_calibration_responses():
    """Ensure the complete SA-001 calibration set remains present."""
    assert len(SA001_RESPONSES) == 5

SA001_HUMAN_GOLD = {
    "R1": {"Accuracy": 1, "Client Context": 0, "Compliance": 0, "Objectives": 1, "Risk": 0, "Affordability": 0, "Clarity": 3, "Yield/Outcome": 0},
    "R2": {"Accuracy": 3, "Client Context": 1, "Compliance": 1, "Objectives": 2, "Risk": 0, "Affordability": 1, "Clarity": 4, "Yield/Outcome": 1},
    "R3": {"Accuracy": 4, "Client Context": 3, "Compliance": 0, "Objectives": 3, "Risk": 2, "Affordability": 4, "Clarity": 4, "Yield/Outcome": 2},
    "R4": {"Accuracy": 4, "Client Context": 5, "Compliance": 4, "Objectives": 5, "Risk": 3, "Affordability": 5, "Clarity": 5, "Yield/Outcome": 3},
    "R5": {"Accuracy": 5, "Client Context": 5, "Compliance": 5, "Objectives": 5, "Risk": 5, "Affordability": 5, "Clarity": 5, "Yield/Outcome": 5},
}

CURRENT_AUTOMATED_TOTALS = {
    "R1": 15,
    "R2": 23,
    "R3": 23,
    "R4": 33,
    "R5": 32,
}

def test_sa001_human_gold_is_explicit():
    """Protect the human calibration labels from accidental changes."""
    assert set(SA001_HUMAN_GOLD) == {"R1", "R2", "R3", "R4", "R5"}
    for gold in SA001_HUMAN_GOLD.values():
        assert set(gold) == set(DIMENSIONS)
        assert all(0 <= score <= 5 for score in gold.values())

    assert [sum(SA001_HUMAN_GOLD[f"R{i}"].values()) for i in range(1, 6)] == [
        5, 13, 22, 34, 40
    ]

def test_sa001_current_scores_match_recorded_baseline():
    """Protect the current evaluator outputs used in disagreement analysis."""
    scenario = load_sa001_scenario()

    for i, response_param in enumerate(SA001_RESPONSES, 1):
        response = response_param.values[0]
        result = evaluate_response(scenario, response)
        assert result.total == CURRENT_AUTOMATED_TOTALS[f"R{i}"]

def test_sa001_disagreement_is_explicit():
    """Report dimension-level disagreement without treating the evaluator as gold."""
    scenario = load_sa001_scenario()

    print("\n--- SA-001 HUMAN VS AUTOMATED ---")
    for i, response_param in enumerate(SA001_RESPONSES, 1):
        response = response_param.values[0]
        result = evaluate_response(scenario, response)
        gold = SA001_HUMAN_GOLD[f"R{i}"]
        disagreements = {
            dimension: (gold[dimension], result.scores[dimension])
            for dimension in DIMENSIONS
            if gold[dimension] != result.scores[dimension]
        }
        print(f"R{i}: gold={sum(gold.values())}/40, automated={result.total}/40")
        print(f"    disagreements={disagreements}")

def test_sa001_objectives_scores_match_recorded_baseline():
    """Protect current Objectives outputs before the calibration experiment."""
    scenario = load_sa001_scenario()
    expected = {"R1": 2, "R2": 3, "R3": 4, "R4": 4, "R5": 4}

    for i, response_param in enumerate(SA001_RESPONSES, 1):
        response = response_param.values[0]
        result = evaluate_response(scenario, response)
        assert result.scores["Objectives"] == expected[f"R{i}"]
