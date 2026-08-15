import pytest

from ai_quality_mcp.server import check_value, simulate_pipeline


def test_check_value_success():
    result = check_value(42)

    assert result == "Value 42 is valid"


def test_check_value_rejects_negative():
    with pytest.raises(ValueError, match="greater than or equal to 0"):
        check_value(-1)


def test_check_value_rejects_value_above_100():
    with pytest.raises(ValueError, match="less than or equal to 100"):
        check_value(101)


def test_pipeline_success():
    result = simulate_pipeline("success")

    assert result == "Pipeline completed successfully"


def test_pipeline_controlled_failure():
    with pytest.raises(RuntimeError, match="Simulated pipeline failure"):
        simulate_pipeline("failure")


def test_pipeline_rejects_invalid_status():
    with pytest.raises(ValueError, match="status must be"):
        simulate_pipeline("banana")
