"""
Content layer for cv-mcp on Cloudflare Workers.

Loads CV markdown files from the content/ directory and builds an in-memory
SQLite FTS5 index for full-text search. This module is designed for lazy
initialization — instantiate ContentIndex on first request, not at module level.

Key difference from the original src/cv_mcp/content.py: file paths are resolved
relative to the Worker bundle root, and initialization is explicit (not at import
time) to avoid Pyodide entropy restrictions during the deploy-time snapshot.
"""

import sqlite3
from pathlib import Path


# Section descriptions — static metadata for list_sections responses.
_SECTION_DESCRIPTIONS: dict[str, str] = {
    "profile": "Identity, bio, contact, certifications, awards, languages",
    "experience": "Roles and organizations, with dates and key work",
    "work": "Patents, publications, talks, standards delegate work, teaching",
    "tech": "Technologies and partner companies, with usage context",
    "narrative": "Career narrative arc, organized in phases",
}


class ContentIndex:
    """
    Encapsulates loaded CV content and FTS5 search index.

    Usage:
        index = ContentIndex()  # loads files + builds index
        index.list_sections()
        index.get_section("profile")
        index.search("kubernetes")
    """

    def __init__(self, content_dir: str | Path | None = None):
        """
        Load markdown files and build FTS5 index.

        Args:
            content_dir: Path to directory containing *.md files.
                         Defaults to content/ sibling to this module.
        """
        if content_dir is None:
            # In Workers, all src/ files end up in the same metadata dir.
            # content/ is a subdirectory relative to this file's location.
            content_dir = Path(__file__).resolve().parent / "content"
        else:
            content_dir = Path(content_dir)

        self._sections: dict[str, str] = {}
        self._db: sqlite3.Connection

        self._load(content_dir)

    def _load(self, content_dir: Path) -> None:
        """Load markdown files and build the FTS5 search index."""
        # Load all .md files from content directory.
        for path in sorted(content_dir.glob("*.md")):
            name = path.stem
            self._sections[name] = path.read_text(encoding="utf-8")

        # Build in-memory FTS5 index.
        self._db = sqlite3.connect(":memory:", check_same_thread=False)
        self._db.execute("CREATE VIRTUAL TABLE cv_fts USING fts5(section, content)")
        for name, text in self._sections.items():
            self._db.execute(
                "INSERT INTO cv_fts(section, content) VALUES (?, ?)", (name, text)
            )
        self._db.commit()

    def list_sections(self) -> list[dict]:
        """Return name and description for each loaded section."""
        return [
            {"name": name, "description": desc}
            for name, desc in _SECTION_DESCRIPTIONS.items()
            if name in self._sections
        ]

    def get_section(self, name: str) -> str:
        """
        Return the full markdown content of a section.
        Raises KeyError if the section name is not found.
        """
        if name not in self._sections:
            raise KeyError(
                f"Section '{name}' not found. "
                f"Available: {list(self._sections.keys())}"
            )
        return self._sections[name]

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Full-text search across all sections.

        Returns matches with snippets and BM25 relevance scores
        (higher = more relevant, scores are negated from FTS5's convention).
        """
        cursor = self._db.execute(
            """
            SELECT
                section,
                snippet(cv_fts, 1, '', '', '...', 32) as snippet,
                bm25(cv_fts) as score
            FROM cv_fts
            WHERE cv_fts MATCH ?
            ORDER BY bm25(cv_fts)
            LIMIT ?
            """,
            (query, top_k),
        )
        return [
            {"section": row[0], "snippet": row[1], "score": -row[2]}
            for row in cursor.fetchall()
        ]
