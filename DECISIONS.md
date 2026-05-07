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

The deployed MCP server uses the Streamable HTTP transport rather than stdio-only. Stdio works for local connections (Claude Desktop → local process) but cannot be accessed over the network. Streamable HTTP exposes the MCP protocol over standard HTTPS, which means any MCP client anywhere can connect without running a local process. Stateless mode is enabled so requests are independent — no session affinity, no in-memory state between requests.

## Cloudflare Workers over a long-running server

The server runs on Cloudflare Workers (Python/Pyodide) rather than a containerized process on Fly.io. Workers provide: zero cold-start cost for warm isolates (3–6ms), no container management, no machine autoscaling config, global edge deployment, and the free tier covers this use case entirely. The tradeoff is the Pyodide runtime constraints (WASM, no arbitrary C extensions), but the dependency footprint (Pydantic + sqlite3) fits within those constraints.

## Cloudflare Workers migration: stateless Streamable HTTP without MCP SDK

The Workers deployment implements the MCP Streamable HTTP transport directly as a plain JSON-RPC 2.0 handler, without importing the `mcp` Python package. This is the "Option D" from the Phase 1 feasibility report.

**Why no MCP SDK**: The `mcp` package's dependency chain (`jsonschema` → `rpds`) calls `getRandomValues` during import, which is forbidden in Cloudflare Workers' deploy-time snapshot phase. Importing lazily at request time works but adds ~4s cold start. Since stateless MCP is just three JSON-RPC methods over HTTP POST, implementing them directly avoids the dependency entirely and gives near-zero cold start.

**Why stateless mode**: The MCP specification (https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/#streamable-http) allows servers to operate without sessions. In stateless mode: no `Mcp-Session` header, no SSE event streams, no GET/DELETE session management. Each POST is self-contained. This maps perfectly to Workers' stateless execution model (no in-memory state between requests from different isolates) and eliminates the need for Durable Objects or external session storage.

**Why Pydantic for validation only**: Pydantic snapshots cleanly at deploy time (no entropy calls). We use it only for input validation of tool arguments at the system boundary, not for response serialization. Tool responses are plain dicts matching the MCP TextContent schema.

**Lazy initialization pattern**: Both content loading (file I/O) and FTS5 index construction happen on first request per isolate, not at module level. A module-level `_index: ContentIndex | None = None` variable caches the result. SQLite's `connect(":memory:")` requires entropy, which is only available at request time in the Workers runtime. First request pays ~50–100ms init; subsequent requests in the same isolate are sub-10ms.
