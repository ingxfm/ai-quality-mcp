FROM python:3.14-slim

# Show output (Docker logs) immediately.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv.
# Installing uv, copying dependency files and
# installing dependencies is done separately,
# so that Docker separates these steps into layers,
# this can save us time if we need rebuild the image,
# the dependency layer can be reused, in case, we just
# changed the HTML page.
COPY --from=ghcr.io/astral-sh/uv:0.12.4 /uv /uvx /bin/

# Copy dependency files first for Docker layer caching.
COPY pyproject.toml uv.lock README.md ./

# Install project dependencies without installing the project yet.
RUN uv sync --locked --no-install-project


# Copy application source.
COPY src ./src

# Copy the demo data
COPY customers.csv ./

# Install the project itself
RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "ai_quality_mcp.web:app", "--host", "0.0.0.0", "--port", "8000"]