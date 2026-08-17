from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import bleach
import markdown

from ai_quality_mcp.agent import run_quality_investigation


app = FastAPI(title="AI Quality Engineer Demo")


HTML_PAGE = (
    Path(__file__).parent / "templates" / "index.html"
).read_text()


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE


@app.post("/investigate")
async def investigate():
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
        "report": safe_report,
    }