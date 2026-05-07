# Roadmap

## v1 — MCP-only (shipped)

The MCP server exposes Francesco Foresta's CV at `mcp.francescoforesta.com`.
Connect from Claude Desktop or any MCP-capable client. See README for setup.

## v1.5 — Web UI (current, shipped)

A public web frontend at `cv.francescoforesta.com` provides a chat
interface for non-technical visitors. Reference implementation lives in
the `feature/web-ui` branch. 

## Future ideas

- Composite MCP tool (`get_relevant_sections`) to reduce round trips when
  the v1.5 web UI is in place.
- Compressed content files for token efficiency.
- Additional content sections as needed.
