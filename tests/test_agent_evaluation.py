import asyncio

from ai_quality_mcp.agent import run_quality_investigation


EXPECTED_FACTS = {
    "duplicate customer id": "2",
    "invalid email": "invalid-email",
    "missing email": "4",
    "negative revenue": "3",
    "invalid revenue": "5",
    "invalid country": "XX"
}


def test_agent_reports_known_data_quality_facts():
    report = asyncio.run(run_quality_investigation())

    report_lower = report.lower()

    missing_facts = []

    for finding, expected_value in EXPECTED_FACTS.items():
        if finding not in report_lower:
            missing_facts.append(finding)
            continue

        if expected_value.lower() not in report_lower:
            missing_facts.append(
                f"{finding} ({expected_value})"
            )

    assert not missing_facts, (
        f"Agent failed to report: {missing_facts}\n\n"
        f"Agent report:\n{report}"
    )

def test_agent_does_not_report_unknown_problem():
    report = asyncio.run(run_quality_investigation())

    assert "duplicate email" not in report.lower()