FROM python:3.12-slim AS builder

RUN pip install uv

WORKDIR /app

# Install dependencies first (layer cache).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and content, then install the project.
COPY src/ src/
COPY content/ content/
COPY README.md ./
RUN uv sync --frozen --no-dev

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV CV_MCP_CONTENT_DIR=/app/content

EXPOSE 8000

CMD ["uvicorn", "cv_mcp.api:app", "--host", "0.0.0.0", "--port", "8000"]
