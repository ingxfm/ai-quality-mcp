import csv
from pathlib import Path

from mcp.server import MCPServer


mcp = MCPServer("AI Quality Demo")

DATA_FILE = Path(__file__).resolve().parents[2] / "customers.csv"


@mcp.tool()
def get_schema() -> dict:
    """Return the expected schema for customer data."""
    return {
        "customer_id": "integer",
        "email": "string",
        "country": "string",
        "revenue": "number",
    }


@mcp.tool()
def check_data_quality() -> dict:
    """
    Check customer data for common quality problems.
    The AI agent calls this function.
    """
    with DATA_FILE.open(newline="") as file:
        customers = list(csv.DictReader(file))

    customer_ids = [row["customer_id"] for row in customers]

    duplicate_ids = {
        customer_id
        for customer_id in customer_ids
        if customer_ids.count(customer_id) > 1
    }

    invalid_emails = [
        row["email"]
        for row in customers
        if "@" not in row["email"]
    ]

    missing_emails = [
        row["customer_id"]
        for row in customers
        if not row["email"]
    ]

    invalid_countries = [
        row["country"]
        for row in customers
        if row["country"] not in {"CZ", "SK"}
    ]

    invalid_revenue = []
    negative_revenue = []

    for row in customers:
        revenue = row["revenue"]

        try:
            revenue_number = float(revenue)
        except ValueError:
            invalid_revenue.append(row["customer_id"])
            continue

        if revenue_number < 0:
            negative_revenue.append(row["customer_id"])

    checks = {
        "duplicate_customer_ids": sorted(duplicate_ids),
        "invalid_emails": invalid_emails,
        "missing_emails": missing_emails,
        "invalid_countries": invalid_countries,
        "invalid_revenue": invalid_revenue,
        "negative_revenue": negative_revenue,
    }

    has_errors = any(checks.values())

    return {
        "status": "FAILED" if has_errors else "PASSED",
        "checks": checks,
        "row_count": len(customers),
    }


@mcp.tool()
def simulate_pipeline(status: str) -> str:
    """Simulate a customer-data pipeline result."""
    if status not in {"success", "failure"}:
        raise ValueError("status must be 'success' or 'failure'")

    if status == "failure":
        raise RuntimeError("Simulated customer pipeline failure")

    return "Customer pipeline completed successfully"


if __name__ == "__main__":
    mcp.run()