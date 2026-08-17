import asyncio
import os
from pathlib import Path

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)
from agents.mcp import MCPServerStdio

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MCP_SERVER_PATH = PROJECT_ROOT / "src" / "ai_quality_mcp" / "server.py"


def create_model() -> OpenAIChatCompletionsModel:
    openrouter_api_key = os.environ["OPENROUTER_API_KEY"]

    openrouter_client = AsyncOpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    return OpenAIChatCompletionsModel(
        model="openrouter/free",
        openai_client=openrouter_client,
    )


async def run_quality_investigation() -> str:
    set_tracing_disabled(True)

    model = create_model()

    mcp_server_parameters = {
        "command": "uv",
        "args": [
            "run",
            "python",
            str(MCP_SERVER_PATH),
        ],
    }

    async with MCPServerStdio(
            name="AI Quality MCP Server",
            params=mcp_server_parameters,
    ) as mcp_server:
        agent = Agent(
            name="AI Quality Engineer",
            instructions="""
            You are an AI Quality Engineer investigating customer data pipelines.
            Use the available MCP tools to investigate the pipeline.
            Do not guess about data quality.
            Use tool results as evidence.
            When you finish:
            1. State whether the pipeline appears healthy.
            2. List every detected data-quality problem.
            3. Identify affected customer IDs when available.
            4. Recommend appropriate regression tests.
            """,
            model=model,
            mcp_servers=[mcp_server],
        )

        result = await Runner.run(
            agent,
            "Investigate the customer data pipeline and report every data-quality problem you find.",
        )
        # print(result.raw_responses)
        ## TODO: change to get the model used, here.
        return result.final_output


async def main():
    report = await run_quality_investigation()

    print("\n=== AI QUALITY ENGINEER REPORT ===\n")
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
