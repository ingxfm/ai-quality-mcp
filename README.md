# MCP server for Agent for CI/CD

What is going is:
"Investigate the customer pipeline."

        ↓

LLM:
"I need information."

        ↓

MCP:
get_schema()

        ↓

MCP:
check_data_quality()

        ↓

MCP:
results

        ↓

LLM:
"These records contain..."


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