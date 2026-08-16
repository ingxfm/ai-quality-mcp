import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MCP_SERVER_PATH = PROJECT_ROOT / "src" / "ai_quality_mcp" / "server.py"


async def call_mcp_tool(tool_name: str, tool_arguments: dict):
    """
    Start the MCP server, connect to it, and call one MCP tool.
    This function is the client.
    """
    server_parameters = StdioServerParameters(
        command="uv",
        args=["run", "python", str(MCP_SERVER_PATH)],
    )

    async with stdio_client(server_parameters) as (
        server_output,
        server_input,
    ):
        async with ClientSession(server_output, server_input) as mcp_session:
            await mcp_session.initialize()

            tool_result = await mcp_session.call_tool(
                tool_name,
                tool_arguments,
            )

            return tool_result


def test_get_schema_returns_response():
    tool_result = asyncio.run(
        call_mcp_tool(
            "get_schema",
            {},
        )
    )

    assert tool_result.is_error is False

    response_text = tool_result.content[0].text

    assert "customer_id" in response_text
    assert "email" in response_text
    assert "country" in response_text
    assert "revenue" in response_text


def test_pipeline_reports_controlled_failure():
    tool_result = asyncio.run(
        call_mcp_tool(
            "simulate_pipeline",
            {"status": "failure"},
        )
    )
    assert tool_result.is_error is True


def test_check_data_quality_detects_known_problems():
    tool_result = asyncio.run(
        call_mcp_tool(
            "check_data_quality",
            {},
        )
    )

    assert tool_result.is_error is False

    import json
    response_data = json.loads(tool_result.content[0].text)

    assert response_data["checks"]["duplicate_customer_ids"] == ["2"]
    assert response_data["checks"]["invalid_emails"] == ["invalid-email", ""]
    assert response_data["checks"]["missing_emails"] == ["4"]
    assert response_data["checks"]["invalid_countries"] == ["XX"]
    assert response_data["checks"]["invalid_revenue"] == ["5"]
    assert response_data["checks"]["negative_revenue"] == ["3"]
    assert response_data["row_count"] == 6