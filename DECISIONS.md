# Design Decisions

## Three tools instead of more

The MCP server exposes exactly three tools: `list_sections`, `get_section`, and `search`. The alternative was finer-grained tools (e.g., per-section getters, separate tools for patents vs. publications, structured queries by date range). Fewer, broader tools work better with LLMs because the model is good at composing multi-step retrieval from simple primitives, and a smaller tool surface reduces selection confusion. Three tools keep the schema compact enough that any model can hold the full tool list in context without truncation. If retrieval patterns prove insufficient in practice, we add tools later — but the starting bias is toward fewer.

## FTS5 over alternatives

The search layer uses SQLite FTS5 (lexical full-text search, in-process). Alternatives considered: vector embeddings with a vector DB (Chroma, FAISS), semantic search via an embedding API, or no search at all (just let the model read all sections). The corpus is under 100KB of markdown — small enough that lexical search finds relevant passages reliably. FTS5 is zero-dependency (bundled with Python's sqlite3), requires no external services, no embedding model, no API calls, and no maintenance as models improve. The search is a convenience for the calling LLM to narrow down which section to read in full, not a precision retrieval system.

## In-memory loading over a database

All five markdown files are loaded into a Python dict at process startup, and the FTS5 index is built in an in-memory SQLite database. The alternative was a persistent SQLite database on disk, or a more complex loading strategy with lazy reads. The corpus is tiny (five files, ~50–100KB total), startup is fast (< 50ms), and there is no write path — content changes only via git push and redeployment. In-memory loading means zero I/O after startup, no file locking concerns, and the simplest possible failure mode: if a file is missing, the process fails to start with a clear error.

## MCP-only for v1, deferring web UI

v1 ships the MCP server alone — no web frontend, no server-side LLM calls. The MCP server is a pure content layer: it serves structured data and lets the calling client (Claude Desktop, or any MCP-capable agent) handle the LLM interaction. This keeps the server stateless, free of API key management, and trivial to operate. A web chat UI (with its own LLM provider, streaming, cost tracking) is deferred to v1.5 in the `feature/web-ui` branch. Shipping MCP-only first validates the content layer in isolation before adding UI complexity.

## Streamable HTTP transport over stdio-only

The deployed MCP server uses the Streamable HTTP transport (MCP SDK's `streamable_http_app()`) rather than stdio-only. Stdio works for local connections (Claude Desktop → local process) but cannot be accessed over the network. Streamable HTTP exposes the MCP protocol over standard HTTPS, which means any MCP client anywhere can connect without running a local process. The tradeoff is needing an HTTP server (FastAPI + uvicorn), but that also gives us a health endpoint and standard deployment tooling. Stateless mode is enabled so requests can be load-balanced across Fly.io machines without session affinity.

## DNS-only (grey cloud) on Cloudflare

The `mcp.francescoforesta.com` CNAME is set to DNS-only (grey cloud) rather than proxied (orange cloud). Fly.io provisions its own TLS certificate via Let's Encrypt, which requires DNS validation or direct connection. Cloudflare's proxy would terminate TLS with its own certificate and re-encrypt to Fly, adding latency and complexity. Since Fly handles TLS natively and the MCP endpoint doesn't need Cloudflare's CDN/WAF features, DNS-only is simpler and eliminates a potential failure mode in certificate renewal.
