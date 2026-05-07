# cv-mcp

MCP server exposing Francesco Foresta's professional CV as a queryable knowledge source.

## Web

A UI connected to the MCP is deployed at [`cv.francescoforesta.com`](https://cv.francescoforesta.com). 

## MCP hands-on? Connect from Claude Desktop

Add this to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cv-mcp": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.francescoforesta.com/mcp"]
    }
  }
}
```

Restart Claude Desktop, then ask: *"What sections does this CV have?"*

> **Note**: `mcp-remote` bridges the remote Streamable HTTP endpoint to Claude Desktop's stdio transport. Requires Node.js installed.

## What's inside

Five curated markdown files covering Francesco's professional background:

| Section | Content |
|---------|---------|
| `profile` | Identity, bio, contact, certifications, awards, languages |
| `experience` | Roles and organizations with dates and key achievements |
| `work` | Patents, publications, talks, standards work |
| `tech` | Technologies and partner companies with usage context |
| `narrative` | Career arc organized in phases |

Three MCP tools expose this content:

| Tool | Purpose |
|------|---------|
| `list_sections` | Discover available sections and their descriptions |
| `get_section` | Read the full markdown of a section by name |
| `search` | Full-text search across all sections (BM25 ranking) |

## Local development

### MCP Server

```bash
cd workers
uv run pywrangler dev
# MCP endpoint: http://localhost:8787/mcp
# Health check: http://localhost:8787/health
```

### Web UI

```bash
cd web
npm install
npm run dev
# http://localhost:5173
```

## Architecture

```
┌──────────────────────┐     Streamable HTTP      ┌──────────────────────┐
│   cv.francescoforesta│    (JSON-RPC 2.0)        │  mcp.francescoforesta│
│        .com          │ ──────────────────────►   │        .com/mcp      │
│                      │                          │                      │
│  Web Chat UI         │                          │  MCP Server          │
│  (agents-starter)    │                          │  (Python/Pyodide)    │
│  Workers AI (Kimi)   │                          │  SQLite FTS5 search  │
│  Durable Objects     │                          │  5 CV sections       │
│  WebSocket + React   │                          │  Stateless           │
└──────────────────────┘                          └──────────────────────┘
       web/                                              workers/
```

Cloudflare Workers (Python/Pyodide). Content files are loaded into memory on first request and indexed with SQLite FTS5 (in-process, zero external dependencies). The MCP server implements Streamable HTTP transport as plain JSON-RPC 2.0 — no `mcp` package, no FastAPI, no uvicorn. Stateless mode: each request is independent. No LLM calls happen server-side — the MCP server only serves content; the calling client (Claude Desktop or similar) handles LLM interaction.

The **web UI** (`web/`) is a chat interface built with `cloudflare/agents-starter` (React 19, Tailwind CSS, `agents` SDK). It connects to the MCP server at startup, discovers the 3 tools, and uses Workers AI (`@cf/moonshotai/kimi-k2.6`) to answer questions about Francesco's CV. Chat history persists via Durable Objects with SQLite.

See [DECISIONS.md](DECISIONS.md) for detailed design rationale.

## Deployment

### MCP Server

Deployed on Cloudflare Workers at `mcp.francescoforesta.com`. Auto-deploys on push to `main` via GitHub Actions.

```bash
cd workers
uv run pywrangler deploy
```

### Web UI

```bash
cd web
npm run deploy
```

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT
