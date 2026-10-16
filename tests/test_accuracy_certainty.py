from tests.test_sa001_calibration import load_sa001_scenario
from accuracy.scoring import evaluate_response


def test_detects_guarantees_returns_claim():
    result = evaluate_response(
        load_sa001_scenario(),
        "This investment guarantees returns.",
    )
    assert result.scores["Accuracy"] == 2
    assert any("excessive certainty" in flag for flag in result.critical_flags)


def test_detects_will_grow_claim():
    result = evaluate_response(
        load_sa001_scenario(),
        "This investment will grow.",
    )
    assert result.scores["Accuracy"] == 2
    assert any("excessive certainty" in flag for flag in result.critical_flags)


def test_detects_no_risk_claim():
    result = evaluate_response(
        load_sa001_scenario(),
        "This investment has no risk.",
    )
    assert result.scores["Accuracy"] == 2
    assert any("excessive certainty" in flag for flag in result.critical_flags)


def test_responsible_uncertainty_caveat_is_not_flagged():
    result = evaluate_response(
        load_sa001_scenario(),
        "Returns are not guaranteed and depend on market conditions.",
    )
    assert not any("excessive certainty" in flag for flag in result.critical_flags)


def test_detects_certain_return_claim():
    result = evaluate_response(
        load_sa001_scenario(),
        "This investment will provide a certain return.",
    )
    assert result.scores["Accuracy"] == 2
    assert any("excessive certainty" in flag for flag in result.critical_flags)
