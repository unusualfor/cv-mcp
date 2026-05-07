"""LLM provider abstraction with streaming support."""

import json
import os
from abc import ABC, abstractmethod
from collections.abc import Iterator

import anthropic
from google import genai
from google.genai import types as gtypes

from cv_mcp import content
from cv_mcp.prompts import SYSTEM_PROMPT

# --- Shared tool execution ---


def execute_tool(name: str, input_data: dict) -> str:
    """Execute a tool call and return the result as a string."""
    if name == "list_sections":
        result = content.list_sections()
    elif name == "get_section":
        try:
            result = content.get_section(input_data["name"])
        except KeyError as e:
            result = {"error": str(e)}
    elif name == "search":
        result = content.search(input_data["query"], input_data.get("top_k", 5))
    else:
        result = {"error": f"Unknown tool: {name}"}

    if isinstance(result, str):
        return result
    return json.dumps(result)


# --- Abstract provider ---


class LLMProvider(ABC):
    """Abstract base for LLM providers with tool-use loop and streaming."""

    @abstractmethod
    def chat_stream(self, messages: list[dict]) -> Iterator[str]:
        """Stream text deltas from the LLM, handling tool calls internally.

        Yields text chunks as they arrive. Tool calls are executed server-side
        and fed back to the model transparently — the caller only sees text.
        """
        ...


# --- Anthropic provider ---

_ANTHROPIC_TOOLS = [
    {
        "name": "list_sections",
        "description": (
            "List all available CV sections with their descriptions. "
            "Call this first to discover what content is available."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_section",
        "description": (
            "Get the full markdown content of a specific CV section by name. "
            "Valid names: profile, experience, work, tech, narrative."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Section name"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "search",
        "description": (
            "Full-text search across all CV sections. Returns matching snippets "
            "with section names and relevance scores (higher = more relevant)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "top_k": {
                    "type": "integer",
                    "description": "Max results to return",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
]


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider with streaming and tool use."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")

    def chat_stream(self, messages: list[dict]) -> Iterator[str]:
        while True:
            # Stream the response.
            collected_content = []
            current_text = ""
            stop_reason = None

            with self.client.messages.stream(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=_ANTHROPIC_TOOLS,
                messages=messages,
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            yield event.delta.text

                # Get the final message after stream completes.
                response = stream.get_final_message()
                stop_reason = response.stop_reason
                collected_content = response.content

            # If end_turn, we're done (text already yielded).
            if stop_reason == "end_turn":
                return

            # If tool_use, execute tools and continue.
            if stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": collected_content})
                tool_results = []
                for block in collected_content:
                    if block.type == "tool_use":
                        result = execute_tool(block.name, block.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result,
                            }
                        )
                messages.append({"role": "user", "content": tool_results})
            else:
                # Unexpected stop reason — done.
                return


# --- Google GenAI provider ---

_GOOGLE_TOOLS = gtypes.Tool(
    function_declarations=[
        gtypes.FunctionDeclaration(
            name="list_sections",
            description=(
                "List all available CV sections with their descriptions. "
                "Call this first to discover what content is available."
            ),
            parameters=gtypes.Schema(
                type="OBJECT", properties={}, required=[]
            ),
        ),
        gtypes.FunctionDeclaration(
            name="get_section",
            description=(
                "Get the full markdown content of a specific CV section by name. "
                "Valid names: profile, experience, work, tech, narrative."
            ),
            parameters=gtypes.Schema(
                type="OBJECT",
                properties={
                    "name": gtypes.Schema(type="STRING", description="Section name"),
                },
                required=["name"],
            ),
        ),
        gtypes.FunctionDeclaration(
            name="search",
            description=(
                "Full-text search across all CV sections. Returns matching snippets "
                "with section names and relevance scores (higher = more relevant)."
            ),
            parameters=gtypes.Schema(
                type="OBJECT",
                properties={
                    "query": gtypes.Schema(type="STRING", description="Search query"),
                    "top_k": gtypes.Schema(type="INTEGER", description="Max results"),
                },
                required=["query"],
            ),
        ),
    ]
)


class GoogleProvider(LLMProvider):
    """Google GenAI provider (Gemma 4) with streaming and tool use."""

    def __init__(self):
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = os.environ.get("GOOGLE_MODEL", "gemini-2.5-flash")

    def chat_stream(self, messages: list[dict]) -> Iterator[str]:
        # Convert messages to Google GenAI format.
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                gtypes.Content(role=role, parts=[gtypes.Part(text=msg["content"])])
            )

        config = gtypes.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[_GOOGLE_TOOLS],
            max_output_tokens=4096,
        )

        while True:
            # Stream the response, accumulating function calls.
            function_calls = []
            model_parts = []

            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=config,
            ):
                if not chunk.candidates:
                    continue
                for part in chunk.candidates[0].content.parts or []:
                    if part.function_call:
                        function_calls.append(part)
                        model_parts.append(part)
                    elif part.text:
                        yield part.text
                        model_parts.append(part)

            # If no function calls, we're done.
            if not function_calls:
                return

            # Append model's response to conversation.
            contents.append(gtypes.Content(role="model", parts=model_parts))

            # Execute function calls and build response.
            function_response_parts = []
            for part in function_calls:
                fc = part.function_call
                args = dict(fc.args) if fc.args else {}
                result = execute_tool(fc.name, args)
                try:
                    parsed = json.loads(result) if isinstance(result, str) else result
                except (json.JSONDecodeError, TypeError):
                    parsed = result
                if isinstance(parsed, dict):
                    result_dict = parsed
                else:
                    result_dict = {"result": parsed}
                function_response_parts.append(
                    gtypes.Part(
                        function_response=gtypes.FunctionResponse(
                            name=fc.name, response=result_dict
                        )
                    )
                )

            contents.append(
                gtypes.Content(role="user", parts=function_response_parts)
            )


# --- Provider factory ---


def get_provider() -> LLMProvider:
    """Create the appropriate LLM provider based on environment configuration.

    Priority: LLM_PROVIDER env var > auto-detect from API keys.
    Default (when both keys are set): Google/Gemma 4.
    """
    provider_name = os.environ.get("LLM_PROVIDER", "").lower()

    if not provider_name:
        # Auto-detect: prefer Google (Gemma 4) as production default.
        if os.environ.get("GOOGLE_API_KEY"):
            provider_name = "google"
        elif os.environ.get("ANTHROPIC_API_KEY"):
            provider_name = "anthropic"
        else:
            raise RuntimeError(
                "No LLM provider configured. Set GOOGLE_API_KEY or ANTHROPIC_API_KEY."
            )

    if provider_name == "google":
        return GoogleProvider()
    elif provider_name == "anthropic":
        return AnthropicProvider()
    else:
        raise RuntimeError(f"Unknown LLM_PROVIDER: {provider_name}")
