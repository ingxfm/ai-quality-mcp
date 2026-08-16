from ai_quality_mcp.server import (
    check_data_quality,
    get_schema,
    simulate_pipeline,
)
import pytest

def test_get_schema():
    schema = get_schema()

    assert schema["customer_id"] == "integer"
    assert schema["email"] == "string"
    assert schema["country"] == "string"
    assert schema["revenue"] == "number"


def test_data_quality_detects_duplicate_customer():
    result = check_data_quality()

    assert result["status"] == "FAILED"
    assert result["checks"]["duplicate_customer_ids"] == ["2"]


def test_data_quality_detects_invalid_email():
    result = check_data_quality()

    assert result["checks"]["invalid_emails"] == ["invalid-email",""]


def test_data_quality_detects_missing_email():
    result = check_data_quality()

    assert result["checks"]["missing_emails"] == ["4"]


def test_data_quality_detects_negative_revenue():
    result = check_data_quality()

    assert result["checks"]["negative_revenue"] == ["3"]


def test_data_quality_detects_invalid_country():
    result = check_data_quality()

    assert result["checks"]["invalid_countries"] == ["XX"]


def test_pipeline_success():
    result = simulate_pipeline("success")

    assert result == "Customer pipeline completed successfully"


def test_pipeline_controlled_failure():
    with pytest.raises(RuntimeError, match="Simulated customer pipeline failure"):
        simulate_pipeline("failure")


def test_pipeline_rejects_invalid_status():
    with pytest.raises(ValueError, match="status must be"):
        simulate_pipeline("banana")