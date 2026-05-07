# cv-mcp

MCP server exposing Francesco Foresta's professional CV as a queryable knowledge source, with a web chat frontend.

## Quick start

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Start the MCP server (stdio)
uv run cv-mcp-server

# Start the full dev environment (backend + frontend)
export GOOGLE_API_KEY="..."   # or ANTHROPIC_API_KEY
./scripts/dev.sh
```

Once running:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/chat
- Health check: http://localhost:8000/health
- MCP endpoint: http://localhost:8000/mcp

## Connecting to Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cv-mcp": {
      "command": "wsl.exe",
      "args": ["-d", "fedoraremix", "--", "/home/francesco/.local/bin/uv", "--directory", "/home/francesco/cv-mcp", "run", "cv-mcp-server"]
    }
  }
}
```

Then restart Claude Desktop and ask: "What sections does this CV have?"

## Project structure

```
content/          # 5 markdown files (profile, experience, work, tech, narrative)
frontend/         # Static HTML/CSS/JS chat UI
src/cv_mcp/
  content.py     # Loads markdown, builds FTS5 index, exposes accessors
  server.py      # MCP server with 3 tool definitions
  api.py         # FastAPI app with SSE streaming chat endpoint
  providers.py   # LLM provider abstraction (Anthropic, Google)
  prompts.py     # System prompt
tests/
  test_content.py
  test_api.py
```

## Tools exposed

| Tool | Description |
|------|-------------|
| `list_sections` | List available CV sections with descriptions |
| `get_section` | Get full markdown content of a section by name |
| `search` | Full-text search across all sections |

## Deployment

### Backend (Fly.io)

The backend deploys automatically on push to `main` (when `src/`, `content/`, or config files change).

```bash
# Manual deploy
flyctl deploy --remote-only

# Set secrets
flyctl secrets set GOOGLE_API_KEY="..." ANTHROPIC_API_KEY="..."
```

- Production URL: `https://cv-mcp.fly.dev`
- Custom domain: `mcp.francescoforesta.com` (CNAME → cv-mcp.fly.dev, DNS-only)

### Frontend (GitHub Pages)

The frontend deploys automatically on push to `main` (when `frontend/` changes).

- Production URL: `https://cv.francescoforesta.com` (CNAME → GitHub Pages, proxied)

### DNS (Cloudflare)

| Record | Name | Target | Proxy |
|--------|------|--------|-------|
| CNAME | `cv` | `<user>.github.io` | Proxied (orange) |
| CNAME | `mcp` | `cv-mcp.fly.dev` | DNS-only (grey) |

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | One of these | Google AI Studio API key |
| `ANTHROPIC_API_KEY` | required | Anthropic API key |
| `GOOGLE_MODEL` | No | Override model (default: `gemini-2.5-flash`) |
| `ANTHROPIC_MODEL` | No | Override model (default: `claude-sonnet-4-5-20250514`) |
| `LLM_PROVIDER` | No | Force provider: `google` or `anthropic` |
| `CV_MCP_CONTENT_DIR` | No | Override content directory path |
