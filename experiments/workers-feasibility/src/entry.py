"""
Feasibility tests for cv-mcp on Cloudflare Workers Python.
Full MCP protocol test - handle a real JSON-RPC request.

KEY FINDING: MCP SDK cannot be imported at module level (deploy-time snapshot)
due to rpds calling getRandomValues. Must use lazy imports at request time.
"""
import json
import sqlite3

from workers import WorkerEntrypoint, Response


# FTS5 index CAN be at module level (no entropy needed)
def _build_index():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE VIRTUAL TABLE sections USING fts5(name, content)")
    conn.execute("INSERT INTO sections VALUES (?, ?)", ("profile", "Francesco Foresta - Cloud Architect"))
    conn.execute("INSERT INTO sections VALUES (?, ?)", ("experience", "JMA Wireless - Principal Architect"))
    return conn

_fts_conn = _build_index()


# MCP must be imported lazily (at request time, not snapshot time)
_mcp_initialized = False
_mcp_tools = None


def _ensure_mcp():
    global _mcp_initialized, _mcp_tools
    if _mcp_initialized:
        return
    from mcp.types import Tool, TextContent
    _mcp_tools = {
        "Tool": Tool,
        "TextContent": TextContent,
    }
    _mcp_initialized = True


class Default(WorkerEntrypoint):
    async def on_fetch(self, request):
        url = str(request.url)
        method = str(request.method)

        if "test-mcp-import" in url:
            return await self.test_mcp_import()
        elif "test-fts5" in url:
            return await self.test_fts5()
        elif "test-mcp-protocol" in url:
            return await self.test_mcp_protocol()
        elif method == "POST" and "/mcp" in url:
            return await self.handle_mcp(request)
        else:
            return Response(json.dumps({
                "status": "ok",
                "tests": ["/test-mcp-import", "/test-fts5", "/test-mcp-protocol", "POST /mcp"]
            }), headers={"Content-Type": "application/json"})

    async def test_mcp_import(self):
        results = {}
        try:
            from mcp.types import Tool, TextContent
            results["mcp.types"] = "OK"
        except Exception as e:
            results["mcp.types"] = f"FAIL: {e}"
        try:
            from mcp.server import Server
            results["mcp.server.Server"] = "OK"
        except Exception as e:
            results["mcp.server.Server"] = f"FAIL: {e}"
        try:
            from pydantic import BaseModel
            results["pydantic"] = "OK"
        except Exception as e:
            results["pydantic"] = f"FAIL: {e}"
        try:
            import anyio
            results["anyio"] = "OK"
        except Exception as e:
            results["anyio"] = f"FAIL: {e}"
        try:
            from starlette.applications import Starlette
            results["starlette"] = "OK"
        except Exception as e:
            results["starlette"] = f"FAIL: {e}"
        try:
            import httpx
            results["httpx"] = "OK"
        except Exception as e:
            results["httpx"] = f"FAIL: {e}"

        all_ok = all(v == "OK" for v in results.values())
        return Response(json.dumps({
            "test": "mcp-import",
            "verdict": "GREEN" if all_ok else "RED",
            "results": results
        }, indent=2), headers={"Content-Type": "application/json"})

    async def test_fts5(self):
        results = {}
        try:
            rows = _fts_conn.execute(
                "SELECT name, content FROM sections WHERE sections MATCH ?", ("architect",)
            ).fetchall()
            results["fts5_query"] = f"OK - found {len(rows)} results"
            results["fts5_data"] = [{"name": r[0], "content": r[1]} for r in rows]
        except Exception as e:
            results["error"] = f"FAIL: {type(e).__name__}: {e}"
        verdict = "GREEN" if "error" not in results else "RED"
        return Response(json.dumps({
            "test": "sqlite-fts5",
            "verdict": verdict,
            "results": results
        }, indent=2), headers={"Content-Type": "application/json"})

    async def test_mcp_protocol(self):
        """Test: Full MCP protocol with lazy imports"""
        results = {}
        try:
            _ensure_mcp()
            Tool = _mcp_tools["Tool"]
            TextContent = _mcp_tools["TextContent"]

            tool = Tool(
                name="test_tool",
                description="A test",
                inputSchema={"type": "object", "properties": {}}
            )
            results["tool_creation"] = "OK"
            results["tool_json"] = tool.model_dump()

            content = TextContent(type="text", text="Hello Workers!")
            results["content_creation"] = "OK"
            results["content_json"] = content.model_dump()
        except Exception as e:
            results["error"] = f"FAIL: {type(e).__name__}: {e}"

        verdict = "GREEN" if "error" not in results else "RED"
        return Response(json.dumps({
            "test": "mcp-protocol",
            "verdict": verdict,
            "results": results
        }, indent=2), headers={"Content-Type": "application/json"})

    async def handle_mcp(self, request):
        """Handle real MCP JSON-RPC requests (Streamable HTTP stateless)"""
        try:
            _ensure_mcp()
            Tool = _mcp_tools["Tool"]
            TextContent = _mcp_tools["TextContent"]

            body = await request.json()
            body_dict = dict(body)
            method = body_dict.get("method", "")
            req_id = body_dict.get("id")

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {"name": "cv-mcp-workers", "version": "0.1.0"}
                    }
                }
            elif method == "tools/list":
                tools = [
                    Tool(
                        name="list_sections",
                        description="List available CV sections",
                        inputSchema={"type": "object", "properties": {}}
                    ),
                    Tool(
                        name="search",
                        description="Search CV content",
                        inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
                    ),
                ]
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [t.model_dump() for t in tools]
                    }
                }
            elif method == "tools/call":
                params = body_dict.get("params", {})
                tool_name = params.get("name", "")
                tool_args = dict(params.get("arguments", {}))

                if tool_name == "search":
                    query = tool_args.get("query", "")
                    rows = _fts_conn.execute(
                        "SELECT name, content FROM sections WHERE sections MATCH ?",
                        (query,)
                    ).fetchall()
                    text = json.dumps([{"name": r[0], "snippet": r[1]} for r in rows])
                elif tool_name == "list_sections":
                    rows = _fts_conn.execute("SELECT DISTINCT name FROM sections").fetchall()
                    text = json.dumps([r[0] for r in rows])
                else:
                    text = f"Unknown tool: {tool_name}"

                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [TextContent(type="text", text=text).model_dump()]
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            return Response(
                json.dumps(response),
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            return Response(
                json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}),
                headers={"Content-Type": "application/json"},
                status=500
            )
