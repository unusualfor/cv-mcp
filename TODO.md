# TODO

## cv-mcp — cost optimization TODOs

### 1. Enable Anthropic prompt caching
- [ ] Mark the system prompt and tool definitions as cached in API calls (`cache_control: {"type": "ephemeral"}` on those blocks).
- [ ] Verify cache hits in logs/metrics — first call pays full price, subsequent calls within ~5 min hit cache at 1/10 input cost.
Expected impact: 50–70% input cost reduction on multi-turn / multi-tool-call queries.

### 2. Compress content files for token efficiency
- [ ] Re-pass `content/*.md` to remove redundant whitespace, collapse over-long bullet lists, tighten verbose phrasing.
Target: ~30% token reduction per section without losing factual content.
- [ ] Validate that tool responses still read naturally to the model.

### 3. Add a composite tool to reduce round trips
- [ ] Introduce a new MCP tool `get_relevant_sections(query: str) -> list[{section, content}]` that internally runs FTS5 search and returns the full content of the top-matching sections in one call.
- [ ] Update tool descriptions so the model prefers this for "open" questions and falls back to `search` + `get_section` only for narrow lookups.
Expected impact: typical query drops from 3 round trips to 1–2.

### Observability prerequisite (do first)
- [ ] Add per-request logging of: provider, model, input tokens, output tokens, cached tokens, tool calls made, total cost.
Without this, optimization is guesswork. With it, every change is measurable.

## UI / Frontend Polish (post-deploy)

- [ ] Formatting: handle markdown rendering in chat responses (bold, links, lists)
- [ ] Loading indicator / typing animation while streaming
- [ ] Error display styling (currently raw text)
- [ ] Mobile responsive layout adjustments
- [ ] Input field auto-resize for multiline
- [ ] Scroll-to-bottom on new messages
- [ ] Accessibility: focus management, ARIA labels
- [ ] Light/dark theme support

## Content
- [ ] Review content
  
