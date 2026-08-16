from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from ai_quality_mcp.agent import run_quality_investigation


app = FastAPI(title="AI Quality Engineer Demo")


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Quality Engineer Demo</title>
</head>
<body>
    <h1>AI Quality Engineer Demo</h1>

    <p>
        Investigate the customer data pipeline using
        an AI agent and MCP quality tools.
    </p>

    <button onclick="console.log('BUTTON WORKS'); investigatePipeline()">
    Investigate Pipeline
    </button>

    <pre id="result">Ready to investigate.</pre>

    <script>
    console.log("SCRIPT LOADED");

    async function investigatePipeline() {
        const resultElement = document.getElementById("result");

        resultElement.textContent =
            "Investigating pipeline... " +
            "The AI agent is running MCP quality checks.";

        console.log("Starting investigation...");

        try {
            const response = await fetch("/investigate", {
                method: "POST"
            });

            console.log("Response received:", response.status);

            const responseText = await response.text();

            console.log("Raw response:", responseText);

            if (!response.ok) {
                throw new Error(
                    `Server returned ${response.status}: ${responseText}`
                );
            }

            const data = JSON.parse(responseText);

            console.log("Parsed response:", data);

            resultElement.textContent = data.report;

        } catch (error) {
            console.error("Investigation failed:", error);

            resultElement.textContent =
                "Investigation failed: " + error.message;
        }
    }

    console.log(
        "investigatePipeline:",
        typeof investigatePipeline
    );
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE


@app.post("/investigate")
async def investigate():
    print(">>> Investigation requested")

    report = await run_quality_investigation()

    print(">>> Investigation completed")

    return {
        "report": report,
    }