"""FastAPI web endpoint for the CV chat interface."""

import json
from collections.abc import Iterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from cv_mcp.providers import get_provider
from cv_mcp.server import mcp as mcp_server

# Build the MCP ASGI app (creates session manager).
_mcp_app = mcp_server.streamable_http_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_server.session_manager.run():
        yield


app = FastAPI(title="cv-mcp", lifespan=lifespan)

# Mount MCP sub-app at /mcp. Its internal route is "/" so the full path is /mcp.
# Lifespan is managed by the parent app above; disable the sub-app's to avoid double-start.
_mcp_app.router.on_startup = []
_mcp_app.router.on_shutdown = []
_mcp_app.router.lifespan_handler = None
app.mount("/mcp", _mcp_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
        "https://cv.francescoforesta.com",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


def _sse_stream(messages: list[dict]) -> Iterator[str]:
    """Generate SSE events from the provider's streaming response."""
    provider = get_provider()
    try:
        for chunk in provider.chat_stream(messages):
            # Escape newlines in the data field for SSE.
            data = json.dumps({"type": "delta", "text": chunk})
            yield f"data: {data}\n\n"
        # Signal end of stream.
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    except Exception as e:
        error_data = json.dumps({"type": "error", "message": str(e)})
        yield f"data: {error_data}\n\n"


@app.post("/api/chat")
def chat(req: ChatRequest):
    # Build messages from history + current message.
    messages = []
    for entry in req.history:
        messages.append({"role": entry["role"], "content": entry["content"]})
    messages.append({"role": "user", "content": req.message})

    return StreamingResponse(
        _sse_stream(messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
