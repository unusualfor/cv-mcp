# cv-mcp — Cloudflare Workers

MCP server exposing Francesco's CV content via the [Streamable HTTP transport](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/#streamable-http). Runs on Cloudflare Workers (Python) with no `mcp` package — plain JSON-RPC 2.0.

## Connecting from Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json` (Linux) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "cv-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.francescoforesta.com/mcp"
      ]
    }
  }
}
```

Requires Node.js 18+ (for `npx`). The `mcp-remote` package is fetched automatically on first use.

## Tools

| Tool | Description |
|------|-------------|
| `list_sections` | List available CV sections with descriptions |
| `get_section` | Get full markdown content of a named section |
| `search` | FTS5 full-text search across all sections |

## Development

```bash
cd workers
uv run pywrangler dev
```

Local server at http://localhost:8787. Hot-reloads on file changes.

## Deploy

```bash
cd workers
uv run pywrangler deploy
```

## Architecture

- **Entry**: `src/entry.py` — JSON-RPC dispatcher, MCP protocol handlers
- **Content**: `src/content.py` — loads markdown files, builds in-memory FTS5 index
- **Content files**: `src/content/*.md` — bundled as Data blobs via wrangler rules
- **No `mcp` package**: Option D — pure JSON-RPC 2.0, Pydantic for input validation only
- **Stateless**: No sessions, no SSE, no state between requests
- **Cold start**: ~700ms (Pyodide + pydantic + FTS5 build), warm: 3-6ms
