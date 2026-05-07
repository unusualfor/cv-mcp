# Design Decisions

## Three tools instead of more

The MCP server exposes exactly three tools: `list_sections`, `get_section`, and `search`. The alternative was finer-grained tools (e.g., per-section getters, separate tools for patents vs. publications, structured queries by date range). Fewer, broader tools work better with LLMs because the model is good at composing multi-step retrieval from simple primitives, and a smaller tool surface reduces selection confusion. Three tools keep the schema compact enough that any model can hold the full tool list in context without truncation. If retrieval patterns prove insufficient in practice, we add tools later — but the starting bias is toward fewer.

## FTS5 over alternatives

The search layer uses SQLite FTS5 (lexical full-text search, in-process). Alternatives considered: vector embeddings with a vector DB (Chroma, FAISS), semantic search via an embedding API, or no search at all (just let the model read all sections). The corpus is under 100KB of markdown — small enough that lexical search finds relevant passages reliably. FTS5 is zero-dependency (bundled with Python's sqlite3), requires no external services, no embedding model, no API calls, and no maintenance as models improve. The search is a convenience for the calling LLM to narrow down which section to read in full, not a precision retrieval system.

## In-memory loading over a database

All five markdown files are loaded into a Python dict at process startup, and the FTS5 index is built in an in-memory SQLite database. The alternative was a persistent SQLite database on disk, or a more complex loading strategy with lazy reads. The corpus is tiny (five files, ~50–100KB total), startup is fast (< 50ms), and there is no write path — content changes only via git push and redeployment. In-memory loading means zero I/O after startup, no file locking concerns, and the simplest possible failure mode: if a file is missing, the process fails to start with a clear error.

## Web API calls content layer directly, not via MCP

The `/api/chat` endpoint calls the same `content.py` functions that the MCP server exposes, but directly — it doesn't go through the MCP protocol to invoke tools. The Anthropic SDK's tool-use interface is used to let Claude call the tools, but tool execution is a local function call in the same process. The alternative was having the web API act as an MCP client connecting to the MCP server. That would add latency, protocol overhead, and a failure mode (the internal MCP connection) for zero benefit: both paths serve the same data from the same in-memory store. The MCP endpoint at `/mcp` exists for external MCP clients; internal tool execution stays in-process.

## SSE streaming over WebSockets or buffered responses

The chat endpoint uses Server-Sent Events (SSE) via FastAPI's `StreamingResponse` — each text delta is sent as a JSON-encoded SSE event (`data: {"type":"delta","text":"..."}\n\n`). Alternatives: WebSockets for bidirectional streaming, or buffered JSON responses. SSE wins because the interaction is strictly request/response with a streamed reply — there is no need for server-initiated messages or client-to-server streaming mid-response. SSE works over standard HTTP, passes through all proxies and CDNs without special configuration, and the browser `fetch` + `ReadableStream` API consumes it natively. WebSockets would add connection lifecycle management, reconnection logic, and protocol upgrade complexity for a unidirectional data flow.

## Provider abstraction with ABC and factory

LLM providers are abstracted behind an `LLMProvider` ABC with a single method: `chat_stream(messages) -> Iterator[str]`. A factory function `get_provider()` selects the implementation based on environment variables (GOOGLE_API_KEY → Google, ANTHROPIC_API_KEY → Anthropic). The alternative was hardcoding a single provider or using a plugin/registry system. The ABC pattern keeps each provider self-contained (its own tool format, streaming protocol, and tool-use loop), while the caller (the API layer) sees only text chunks. Adding a new provider means implementing one class and one branch in the factory — no changes to the API layer. The tool-use loop is internal to each provider: the caller never sees tool calls, only the final streamed text.

## Vanilla JS frontend instead of a framework

The frontend is plain HTML, CSS, and JS — no React, no build step, no bundler. The UI is a single chat interface with a text input. A framework would add dependency weight, build complexity, and deployment steps for ~60 lines of interactive logic. The vanilla approach means the frontend is three static files that can be served from any CDN or static host without a build pipeline. If the UI grows significantly in v2 (multi-page, rich formatting, auth flows), a framework might be justified; for v1 it would be over-engineering.
