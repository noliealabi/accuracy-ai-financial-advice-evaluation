import json
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def benchmark_data():
    return json.loads(
        Path("data/benchmark_sa.json").read_text(encoding="utf-8")
    )


def test_count(benchmark_data):
    assert len(benchmark_data) == 81


def test_fields(benchmark_data):
    required_fields = {
        "id",
        "category",
        "scenario",
        "ai_response",
        "critical_errors",
        "expected_considerations",
    }

    for item in benchmark_data:
        assert required_fields.issubset(item)
        assert len(item["expected_considerations"]) == 6


def test_unique_ids(benchmark_data):
    assert len({item["id"] for item in benchmark_data}) == 81
