# Roadmap

## v1 — MCP-only (current, shipped)

The MCP server exposes Francesco Foresta's CV at `mcp.francescoforesta.com`.
Connect from Claude Desktop or any MCP-capable client. See README for setup.

## v1.5 — Web UI (deferred)

A public web frontend at `cv.francescoforesta.com` will provide a chat
interface for non-technical visitors. Reference implementation lives in
the `feature/web-ui` branch. Tasks include:

- FastAPI chat endpoint that wraps the MCP content layer and calls an LLM
  with the three tools attached.
- Streaming response handling (SSE).
- Multi-provider LLM abstraction (Anthropic, Google AI Studio).
- Vanilla HTML/CSS/JS frontend.
- Prompt caching for cost optimization.
- Cloudflare proxy for rate limiting on the chat endpoint.
- Per-request observability (model, tokens in/out, cached tokens, cost).

## Future ideas

- Composite MCP tool (`get_relevant_sections`) to reduce round trips when
  the v1.5 web UI is in place.
- Compressed content files for token efficiency.
- Additional content sections as needed.
