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


def test_check_value_accepts_valid_value():
    tool_result = asyncio.run(
        call_mcp_tool(
            "check_value",
            {"value": 50},
        )
    )
    assert tool_result.content[0].text == "Value 50 is valid"


def test_check_value_rejects_invalid_value():
    tool_result = asyncio.run(
        call_mcp_tool(
            "check_value",
            {"value": -1},
        )
    )
    assert tool_result.is_error is True


def test_pipeline_reports_controlled_failure():
    tool_result = asyncio.run(
        call_mcp_tool(
            "simulate_pipeline",
            {"status": "failure"},
        )
    )
    assert tool_result.is_error is True
