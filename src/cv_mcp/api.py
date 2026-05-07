"""ASGI app that exposes the MCP server over Streamable HTTP."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from cv_mcp.server import mcp as mcp_server

# Build the MCP ASGI app (creates session manager).
_mcp_app = mcp_server.streamable_http_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_server.session_manager.run():
        yield


app = FastAPI(title="cv-mcp", lifespan=lifespan)

# Mount MCP sub-app at /mcp. Its internal route is "/" so the full path is /mcp.
_mcp_app.router.on_startup = []
_mcp_app.router.on_shutdown = []
_mcp_app.router.lifespan_handler = None
app.mount("/mcp", _mcp_app)


@app.get("/health")
def health():
    return {"status": "ok"}

