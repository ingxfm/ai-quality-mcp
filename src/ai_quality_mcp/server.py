from mcp.server import MCPServer


mcp = MCPServer("AI Quality Demo")


@mcp.tool()
def check_value(value: int) -> str:
    """Check whether a numeric value is within the accepted range."""
    if value < 0:
        raise ValueError("value must be greater than or equal to 0")

    if value > 100:
        raise ValueError("value must be less than or equal to 100")

    return f"Value {value} is valid"


@mcp.tool()
def simulate_pipeline(status: str) -> str:
    """Simulate a pipeline result. Accepted statuses: success, failure."""
    if status not in {"success", "failure"}:
        raise ValueError("status must be 'success' or 'failure'")

    if status == "failure":
        raise RuntimeError("Simulated pipeline failure")

    return "Pipeline completed successfully"


if __name__ == "__main__":
    mcp.run()
