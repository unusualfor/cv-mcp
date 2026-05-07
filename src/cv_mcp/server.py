"""MCP server exposing Francesco Foresta's CV via three tools."""

from mcp.server.fastmcp import FastMCP

from cv_mcp import content

mcp = FastMCP("cv-mcp")


@mcp.tool(
    name="list_sections",
    description=(
        "List all available CV sections with their descriptions. "
        "Call this first to discover what content is available before "
        "fetching or searching."
    ),
)
def list_sections() -> list[dict]:
    """List available CV sections."""
    return content.list_sections()


@mcp.tool(
    name="get_section",
    description=(
        "Get the full markdown content of a specific CV section by name. "
        "Use after list_sections or search to read detailed content. "
        "Valid names: profile, experience, work, tech, narrative."
    ),
)
def get_section(name: str) -> str:
    """Fetch a section's full content by name."""
    return content.get_section(name)


@mcp.tool(
    name="search",
    description=(
        "Full-text search across all CV sections. Returns matching snippets "
        "with section names and relevance scores (higher = more relevant). "
        "Use for open-ended questions where you don't know which section is "
        "relevant. Follow up with get_section if you need more context."
    ),
)
def search(query: str, top_k: int = 5) -> list[dict]:
    """Search the CV content."""
    return content.search(query, top_k)


def main():
    """Run the MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
