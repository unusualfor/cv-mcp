"""
cv-mcp — Cloudflare Workers entry point.

Implements the MCP Streamable HTTP transport (stateless mode) as a plain
JSON-RPC 2.0 handler, without importing the `mcp` Python package.

Protocol reference:
  https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/#streamable-http

Design decisions:
  - Option D from Phase 1 feasibility: no `mcp` package import.
  - Stateless mode: every request is an independent JSON-RPC call/response.
    No session IDs, no SSE streaming, no Mcp-Session header.
  - Lazy initialization: content + FTS5 index built on first request per isolate,
    cached in module-level variable for subsequent requests.
  - See DECISIONS.md for rationale.
"""

import json

from workers import Response, WorkerEntrypoint

from content import ContentIndex

# ---------------------------------------------------------------------------
# Lazy-initialized singleton. Set on first request, reused across the isolate.
# ---------------------------------------------------------------------------
_index: ContentIndex | None = None


def _ensure_initialized() -> ContentIndex:
    """Initialize the content index on first invocation; return cached thereafter."""
    global _index
    if _index is None:
        _index = ContentIndex()
    return _index


# ---------------------------------------------------------------------------
# MCP Protocol Constants
# ---------------------------------------------------------------------------
_SERVER_INFO = {
    "name": "cv-mcp",
    "version": "1.0.0",
}
_PROTOCOL_VERSION = "2025-03-26"
_CAPABILITIES = {
    "tools": {"listChanged": False},
}

# Tool definitions — these are the contract with MCP clients.
_TOOLS = [
    {
        "name": "list_sections",
        "description": (
            "List all available CV sections with their descriptions. "
            "Call this first to discover what content is available before "
            "fetching or searching."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "get_section",
        "description": (
            "Get the full markdown content of a specific CV section by name. "
            "Use after list_sections or search to read detailed content. "
            "Valid names: profile, experience, work, tech, narrative."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Section name (e.g. 'profile', 'experience').",
                }
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "search",
        "description": (
            "Full-text search across all CV sections. Returns matching snippets "
            "with section names and relevance scores (higher = more relevant). "
            "Use for open-ended questions where you don't know which section is "
            "relevant. Follow up with get_section if you need more context."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (FTS5 syntax supported).",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Maximum number of results (default 5).",
                    "default": 5,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
]


# ---------------------------------------------------------------------------
# JSON-RPC Helpers
# ---------------------------------------------------------------------------

def _jsonrpc_response(req_id, result: dict) -> dict:
    """Wrap a result in a JSON-RPC 2.0 success envelope."""
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _jsonrpc_error(req_id, code: int, message: str, data=None) -> dict:
    """Wrap an error in a JSON-RPC 2.0 error envelope."""
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": req_id, "error": err}


# ---------------------------------------------------------------------------
# MCP Method Handlers
# ---------------------------------------------------------------------------

async def _handle_initialize(req_id, _params: dict) -> dict:
    """
    Implements: initialize
    Spec: https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle/#initialization

    The client sends this as the first request to negotiate protocol version
    and discover server capabilities. In stateless mode we respond identically
    every time — there is no session to establish.

    Deliberate simplification: we ignore the client's proposed capabilities
    and protocolVersion and always respond with our own. The spec allows the
    server to select the protocol version; we pin to 2025-03-26.
    """
    return _jsonrpc_response(req_id, {
        "protocolVersion": _PROTOCOL_VERSION,
        "capabilities": _CAPABILITIES,
        "serverInfo": _SERVER_INFO,
    })


async def _handle_tools_list(req_id, _params: dict) -> dict:
    """
    Implements: tools/list
    Spec: https://spec.modelcontextprotocol.io/specification/2025-03-26/server/tools/#listing-tools

    Returns the complete list of tools this server exposes. In our case the
    list is static (three tools), so we return it verbatim. The listChanged
    capability is set to False since tools never change at runtime.
    """
    return _jsonrpc_response(req_id, {"tools": _TOOLS})


async def _handle_tools_call(req_id, params: dict) -> dict:
    """
    Implements: tools/call
    Spec: https://spec.modelcontextprotocol.io/specification/2025-03-26/server/tools/#calling-tools

    Dispatches to the appropriate tool handler based on params.name.
    Returns content as a list of TextContent objects per the MCP spec.

    Deliberate simplification: we only return TextContent (type: "text"),
    never ImageContent or EmbeddedResource, since CV data is always text.
    """
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    index = _ensure_initialized()

    try:
        if tool_name == "list_sections":
            result_text = json.dumps(index.list_sections())
        elif tool_name == "get_section":
            name = arguments.get("name", "")
            result_text = index.get_section(name)
        elif tool_name == "search":
            query = arguments.get("query", "")
            top_k = arguments.get("top_k", 5)
            result_text = json.dumps(index.search(query, top_k))
        else:
            return _jsonrpc_error(req_id, -32602, f"Unknown tool: {tool_name}")
    except KeyError as e:
        # Tool executed but failed (e.g. invalid section name).
        return _jsonrpc_response(req_id, {
            "content": [{"type": "text", "text": str(e)}],
            "isError": True,
        })
    except Exception as e:
        return _jsonrpc_response(req_id, {
            "content": [{"type": "text", "text": f"Internal error: {e}"}],
            "isError": True,
        })

    return _jsonrpc_response(req_id, {
        "content": [{"type": "text", "text": result_text}],
    })


# Method dispatch table.
_HANDLERS = {
    "initialize": _handle_initialize,
    "tools/list": _handle_tools_list,
    "tools/call": _handle_tools_call,
}


# ---------------------------------------------------------------------------
# Workers Entry Point
# ---------------------------------------------------------------------------

class Default(WorkerEntrypoint):
    """
    Cloudflare Workers entrypoint for the cv-mcp MCP server.

    All MCP traffic arrives as POST /mcp with a JSON-RPC 2.0 body.
    A GET /health endpoint is provided for monitoring.
    """

    async def on_fetch(self, request):
        url = str(request.url)
        method = str(request.method)

        # Health check endpoint (for monitoring / uptime checks).
        if method == "GET" and url.endswith("/health"):
            return Response(
                json.dumps({"status": "ok"}),
                headers={"Content-Type": "application/json"},
            )

        # MCP endpoint: POST /mcp
        if method == "POST" and "/mcp" in url:
            return await self._handle_mcp(request)

        # Everything else: 404
        return Response("Not Found", status=404)

    async def _handle_mcp(self, request):
        """
        MCP Streamable HTTP transport handler (stateless mode).

        Spec: https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/#streamable-http

        In stateless mode:
        - Client sends POST with JSON-RPC request body.
        - Server responds with JSON-RPC response body (Content-Type: application/json).
        - No session headers, no SSE, no GET/DELETE for session management.
        """
        # Validate content type
        content_type = str(request.headers.get("content-type", ""))
        if "application/json" not in content_type:
            return Response(
                json.dumps(_jsonrpc_error(None, -32700, "Content-Type must be application/json")),
                status=400,
                headers={"Content-Type": "application/json"},
            )

        # Parse request body
        try:
            body = await request.json()
            body_dict = dict(body)
        except Exception:
            return Response(
                json.dumps(_jsonrpc_error(None, -32700, "Parse error: invalid JSON")),
                status=400,
                headers={"Content-Type": "application/json"},
            )

        # Extract JSON-RPC fields
        req_id = body_dict.get("id")
        rpc_method = body_dict.get("method", "")
        params = body_dict.get("params", {})
        if isinstance(params, dict):
            pass
        else:
            params = dict(params) if params else {}

        # Dispatch to handler
        handler = _HANDLERS.get(rpc_method)
        if handler is None:
            response_body = _jsonrpc_error(req_id, -32601, f"Method not found: {rpc_method}")
        else:
            response_body = await handler(req_id, params)

        return Response(
            json.dumps(response_body),
            headers={"Content-Type": "application/json"},
        )
