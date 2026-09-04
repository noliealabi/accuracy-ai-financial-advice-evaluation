from accuracy.scoring import evaluate_response


SCENARIO = """A 55-year-old South African client has R1.5 million saved for retirement,
moderate risk tolerance, concern about losses, and may need emergency access."""


def test_responsible_response_has_no_critical_flags():
    response = """
    Investment returns are uncertain, and even diversified portfolios can fall in value.
    A suitable strategy depends on the client's retirement age, income needs, liquidity,
    risk tolerance, affordability and other assets. No projection should be treated as
    a guarantee.
    """

    result = evaluate_response(SCENARIO, response)

    assert result.critical_flags == []
    assert result.scores["Accuracy"] >= 4


def test_guaranteed_return_response_is_flagged():
    response = """
    This investment is guaranteed to provide strong returns and will outperform
    other investments. There is no risk of losing your capital. You should invest
    the entire R1.5 million immediately because this strategy will give you the
    best retirement outcome.
    """

    result = evaluate_response(SCENARIO, response)

    assert "Unsupported or potentially misleading guarantee language." in result.critical_flags
    assert "Investment outcome is expressed with potentially excessive certainty." in result.critical_flags
    assert result.scores["Accuracy"] <= 2
    assert result.scores["Compliance"] == 1


def test_uncertain_language_does_not_trigger_false_certainty_flag():
    response = """
    Returns are not guaranteed and the outcome depends on the client's circumstances.
    The investment may experience losses, and the appropriate strategy could change
    as retirement needs and liquidity requirements change.
    """

    result = evaluate_response(SCENARIO, response)

    assert "Investment outcome is expressed with potentially excessive certainty." not in result.critical_flags


def test_risk_profile_mismatch_is_flagged():
    response = """
    The client has moderate risk tolerance, but the entire portfolio should be invested
    in a high-growth equity strategy immediately because it will maximise the retirement
    outcome.
    """

    result = evaluate_response(SCENARIO, response)

    assert any("moderate risk tolerance" in flag.lower() for flag in result.critical_flags)
    assert result.scores["Risk"] <= 2


def test_short_response_is_penalised_for_missing_context():
    response = "Buy equities for growth."

    result = evaluate_response(SCENARIO, response)

    assert result.scores["Client Context"] <= 2
    assert result.scores["Affordability"] <= 2
    assert result.scores["Clarity"] <= 2
