# Demo: MCP server for Agent for CI/CD
[![CI](https://github.com/ingxfm/ai-quality-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ingxfm/ai-quality-mcp/actions/workflows/ci.yml)

What is going on is:
```
                         Recruiter
                             │
                             ▼
                    HTTPS Web Interface
                             │
                             ▼
                         FastAPI
                             │
                             ▼
                         AI Agent
                             │
                             ▼
                       MCP Protocol
                       ┌─────┴─────┐
                       ▼           ▼
                Data Quality   Pipeline
                    Tools        Tool
                       │           │
                       └─────┬─────┘
                             ▼
                       Quality Results
                             │
                             ▼
                         AI Report
```
# Diagram
```
User
        ↓

LLM Agent
        ↓
┌─────────────────────┐
│ MCP Server          │
│                     │
│ get_schema()        │
│ check_data_quality()│
│ simulate_pipeline() │
└─────────────────────┘
```
This demo includes:
### Unit / deterministic tests
```
test_server.py
```
Tests the Python functions and expected behavior.

### MCP protocol tests
```
test_mcp_protocol.py
```
Tests the actual MCP client/server communication.

### LLM evaluation
```
test_agent_evaluation.py
```
Tests if the agent produces an acceptable investigation result.

## On GitHub Actions
```
GitHub Push
     │
     ├── Deterministic tests ─────── ✓
     │
     └── Docker build ────── ✓

Manual:
     │
     └── LLM evaluation ──── ✓
```
Deterministic tests are kept separate from the LLM evaluation because that evaluation depends on an external provider (openrouter.ai) free tier. This introduces latency and non-deterministic behavior. There is a 50 request limit per day for the free models. 

## Manually
```CLI
# Run the deterministic tests
uv run pytest tests/test_server.py tests/test_mcp_protocol.py

# Run the LLM evaluation tests
uv run pytest tests/test_agent_evaluation.py
```
