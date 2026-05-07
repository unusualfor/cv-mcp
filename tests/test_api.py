"""Tests for the cv_mcp API layer."""

import json
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Ensure at least one provider key is set for import.
os.environ.setdefault("GOOGLE_API_KEY", "test-key")

from cv_mcp.api import app  # noqa: E402

client = TestClient(app)


def test_health():
    """Health endpoint returns ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def _parse_sse_events(response) -> list[dict]:
    """Parse SSE events from a streaming response."""
    events = []
    for line in response.text.split("\n"):
        if line.startswith("data: "):
            events.append(json.loads(line[6:]))
    return events


def test_chat_streaming_google():
    """Chat endpoint streams SSE events using Google provider."""
    # Mock the Google GenAI client's streaming method.
    mock_chunk = MagicMock()
    mock_part = MagicMock()
    mock_part.function_call = None
    mock_part.text = "Francesco is a software architect."
    mock_chunk.candidates = [MagicMock()]
    mock_chunk.candidates[0].content.parts = [mock_part]

    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key", "LLM_PROVIDER": "google"}):
        with patch("cv_mcp.providers.genai.Client") as MockClient:
            mock_client = MagicMock()
            mock_client.models.generate_content_stream.return_value = iter([mock_chunk])
            MockClient.return_value = mock_client

            response = client.post(
                "/api/chat",
                json={"message": "Who is Francesco?", "history": []},
            )

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    events = _parse_sse_events(response)
    assert len(events) >= 2  # At least one delta + done
    assert events[0]["type"] == "delta"
    assert events[0]["text"] == "Francesco is a software architect."
    assert events[-1]["type"] == "done"


def test_chat_streaming_anthropic():
    """Chat endpoint streams SSE events using Anthropic provider."""

    # Create a mock stream context manager.
    class MockStream:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def __iter__(self):
            # Yield a text delta event.
            event = MagicMock()
            event.type = "content_block_delta"
            event.delta.type = "text_delta"
            event.delta.text = "Hello from Claude."
            yield event

        def get_final_message(self):
            msg = MagicMock()
            msg.stop_reason = "end_turn"
            block = MagicMock()
            block.type = "text"
            block.text = "Hello from Claude."
            msg.content = [block]
            return msg

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key", "LLM_PROVIDER": "anthropic"}):
        with patch("cv_mcp.providers.anthropic.Anthropic") as MockAnthropic:
            mock_client = MagicMock()
            mock_client.messages.stream.return_value = MockStream()
            MockAnthropic.return_value = mock_client

            response = client.post(
                "/api/chat",
                json={"message": "Hello", "history": []},
            )

    assert response.status_code == 200
    events = _parse_sse_events(response)
    assert any(e["type"] == "delta" and "Hello from Claude" in e["text"] for e in events)
    assert events[-1]["type"] == "done"


def test_chat_tool_use_google():
    """Google provider handles tool calls within streaming."""
    from google.genai import types as gtypes

    # First chunk: function call (no text).
    fc_part = gtypes.Part(
        function_call=gtypes.FunctionCall(name="list_sections", args={})
    )
    chunk1 = MagicMock()
    chunk1.candidates = [MagicMock()]
    chunk1.candidates[0].content.parts = [fc_part]

    # Second call (after tool result): text response.
    text_part = gtypes.Part(text="There are 5 sections.")
    chunk2 = MagicMock()
    chunk2.candidates = [MagicMock()]
    chunk2.candidates[0].content.parts = [text_part]

    call_count = [0]

    def mock_stream(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return iter([chunk1])
        else:
            return iter([chunk2])

    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key", "LLM_PROVIDER": "google"}):
        with patch("cv_mcp.providers.genai.Client") as MockClient:
            mock_client = MagicMock()
            mock_client.models.generate_content_stream.side_effect = mock_stream
            MockClient.return_value = mock_client

            response = client.post(
                "/api/chat",
                json={"message": "What sections?", "history": []},
            )

    assert response.status_code == 200
    events = _parse_sse_events(response)
    text_events = [e for e in events if e["type"] == "delta"]
    assert any("5 sections" in e["text"] for e in text_events)
    assert events[-1]["type"] == "done"
    # Model was called twice (initial + after tool result).
    assert mock_client.models.generate_content_stream.call_count == 2
