from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

import asyncio
import bleach
import markdown

from ai_quality_mcp.agent import run_quality_investigation


app = FastAPI(title="AI Quality Engineer Demo")


HTML_PAGE = (
    Path(__file__).parent / "templates" / "index.html"
).read_text()


# Allow only one investigation to run at a time.
investigation_lock = asyncio.Lock()


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE


@app.post("/investigate")
async def investigate():
    if investigation_lock.locked():
        return JSONResponse(
            status_code=409,
            content={
                "busy": True,
                "message": (
                    "An investigation is already running. "
                    "Please wait for the previous response."
                ),
            },
        )

    async with investigation_lock:
        report = await run_quality_investigation()

    html_report = markdown.markdown(
        report,
        extensions=["extra"],
    )

    safe_report = bleach.clean(
        html_report,
        tags=[
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "code",
            "pre",
            "blockquote",
        ],
        attributes={},
    )

    return {
        "busy": False,
        "report": safe_report,
        "model": "openrouter/free",
    }