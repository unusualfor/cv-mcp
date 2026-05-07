# Cloudflare Workers Python — Feasibility Report for cv-mcp

**Date**: 2025-07-07  
**Branch**: `experiment/workers-python`  
**Verdict**: 🟡 YELLOW — Feasible with caveats

---

## Executive Summary

Migration from Fly.io to Cloudflare Workers Python is **technically feasible**.
All core capabilities work. However, there is one significant architectural
constraint that requires a design decision:

1. **MCP SDK and SQLite cannot be imported/initialized at module level** during 
   the deploy-time snapshot due to entropy restrictions (`getRandomValues` blocked 
   in global scope).
2. **First cold-start request takes ~4 seconds** to import MCP SDK (pydantic, 
   jsonschema/rpds). Subsequent requests in the same isolate are 5-10ms.
3. The MCP SDK's built-in HTTP transport (Starlette ASGI) **cannot be used** 
   directly. We must implement a thin JSON-RPC handler ourselves.

---

## Test Results

| Test | Verdict | Details |
|------|---------|---------|
| MCP SDK import (lazy) | ✅ GREEN | All deps (pydantic, anyio, starlette, httpx) import fine at request time |
| SQLite FTS5 | ✅ GREEN | CREATE VIRTUAL TABLE, INSERT, MATCH all work perfectly |
| MCP JSON-RPC protocol | ✅ GREEN | initialize, tools/list, tools/call all produce correct responses |
| Module-level MCP import | ❌ RED | `rpds` (jsonschema dep) calls getRandomValues — fatal at snapshot time |
| Module-level SQLite | ⚠️ WARN | Entropy warning but non-fatal; works at request time regardless |
| Deploy-time snapshot optimization | ⚠️ YELLOW | Cannot snapshot MCP SDK imports → cold start penalty |

---

## Performance Measurements (Local Dev)

| Operation | Latency |
|-----------|---------|
| Root endpoint (no MCP) | 26ms |
| FTS5 query (module-level index) | 21ms |
| **First MCP import (cold start)** | **4007ms** |
| MCP JSON-RPC after import cached | 5-10ms |
| Tool call + FTS5 search | 6ms |

**Note**: Cold start is per-isolate. Once the isolate is warm, all requests are 
sub-10ms. Workers keep isolates alive for minutes between requests.

---

## Architecture: What Changes

### Current (Fly.io)
```
Client → ASGI (uvicorn) → FastAPI → MCP SDK streamable_http_app() → Server
```

### Proposed (Workers)
```
Client → Workers fetch() → Custom JSON-RPC handler → MCP types (pydantic) → FTS5
```

**Key difference**: We bypass the MCP SDK's transport layer (Starlette/ASGI) and 
implement the Streamable HTTP protocol ourselves. This is simple because:
- Stateless mode = one request → one JSON response (no sessions, no SSE)
- The protocol is just JSON-RPC 2.0 over HTTP POST
- We only handle 3 methods: `initialize`, `tools/list`, `tools/call`

---

## Mitigation Strategies for Cold Start

1. **Option A**: Accept 4s first-request latency. Workers keep isolates warm for 
   minutes, so most requests will be fast. Free tier is fine for a personal CV.
   
2. **Option B**: Remove `jsonschema` dependency. The MCP SDK uses it but we can 
   avoid importing `mcp` entirely and just use `pydantic` directly for Tool/TextContent 
   models (they're simple dataclasses). Pydantic imports are likely faster without 
   the jsonschema chain.

3. **Option C**: Use a cron trigger or scheduled Worker to keep the isolate warm.

4. **Option D**: Drop `mcp` package entirely and implement the 3 JSON-RPC methods 
   with plain dicts. Zero dependency cold start. This is viable because stateless 
   MCP is just a thin JSON envelope.

---

## Bundle Size

```
Total (691 modules): 10,817 KiB (~10.5 MB)
```

Workers free tier allows 10MB compressed. The bundle is large but should compress 
well (Python source). **Needs testing on deploy** to confirm it fits.

---

## What We Lose vs Fly.io

| Feature | Fly.io | Workers |
|---------|--------|---------|
| MCP SDK transport layer | Built-in ASGI | Custom (trivial for stateless) |
| Session state (SSE) | Supported | Not needed (stateless mode) |
| Deploy-time import optimization | N/A | Blocked by entropy restriction |
| uvicorn/ASGI | Yes | No (Workers fetch handler) |
| Docker/full Python | Yes | Pyodide (CPython→WASM) |

---

## What We Gain

| Feature | Fly.io | Workers |
|---------|--------|---------|
| Cost | $0 (free tier, but limited) | $0 (100k req/day free) |
| Cold start | ~2s (machine stop/start) | ~4s (MCP import) or sub-100ms (Option D) |
| Warm latency | ~50ms | 5-10ms |
| Edge locations | 1 (fra) | 300+ |
| Auto-scaling | Single machine | Unlimited (free tier) |
| Custom domain | ✅ | ✅ |
| Maintenance | Dockerfile, fly.toml, flyctl | Single .py file + wrangler config |

---

## Recommendation

**Proceed with Option D (no `mcp` package)** for Phase 2:

- Implement the 3 JSON-RPC methods directly with plain Python (no MCP SDK import)
- Use Pydantic for input validation only (it snapshots fine)
- Keep FTS5 for search (works perfectly, just init lazily)
- Result: Near-zero cold start, sub-10ms warm responses, minimal bundle

The MCP Streamable HTTP protocol in stateless mode is trivial:
```python
# The entire protocol is just this:
POST /mcp  {"jsonrpc":"2.0","id":1,"method":"initialize",...}
POST /mcp  {"jsonrpc":"2.0","id":2,"method":"tools/list",...}  
POST /mcp  {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search","arguments":{"query":"..."}}}
```

---

## Files Created

- `experiments/workers-feasibility/src/entry.py` — Working test harness
- `experiments/workers-feasibility/pyproject.toml` — Project config
- `experiments/workers-feasibility/wrangler.jsonc` — Worker config
- `experiments/workers-feasibility/REPORT.md` — This file

---

## Next Steps (Phase 2 — pending your approval)

1. Create `workers/` directory at repo root
2. Implement `src/entry.py` with full cv-mcp logic (no MCP SDK, plain JSON-RPC)
3. Port content.py logic (load markdown, build FTS5 index)  
4. Configure custom domain (mcp.francescoforesta.com)
5. Deploy + test with mcp-remote
6. Remove Fly.io infrastructure
