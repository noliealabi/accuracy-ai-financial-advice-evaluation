import pytest

from accuracy.scoring import DIMENSIONS, evaluate


def test_perfect():
    assert evaluate({dimension: 5 for dimension in DIMENSIONS}).total == 40


def test_critical_override():
    result = evaluate(
        {dimension: 5 for dimension in DIMENSIONS},
        ["flag"],
    )

    assert result.classification.startswith("CRITICAL")


def test_invalid():
    with pytest.raises(ValueError):
        evaluate({dimension: 6 for dimension in DIMENSIONS})
