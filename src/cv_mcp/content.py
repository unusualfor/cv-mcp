"""Content layer: loads CV markdown files and provides FTS5 search."""

import os
import sqlite3
from pathlib import Path

# Resolve content directory: env var override or default relative to project root.
_CONTENT_DIR = Path(
    os.environ.get(
        "CV_MCP_CONTENT_DIR",
        str(Path(__file__).resolve().parent.parent.parent / "content"),
    )
)

# Hardcoded section descriptions (not parsed from files).
_SECTION_DESCRIPTIONS: dict[str, str] = {
    "profile": "Identity, bio, contact, certifications, awards, languages",
    "experience": "Roles and organizations, with dates and key work",
    "work": "Patents, publications, talks, standards delegate work, teaching",
    "tech": "Technologies and partner companies, with usage context",
    "narrative": "Career narrative arc, organized in phases",
}

# In-memory store: section name -> markdown content.
_sections: dict[str, str] = {}

# In-memory SQLite database with FTS5 index.
_db: sqlite3.Connection


def _load() -> None:
    """Load markdown files from content/ and build the FTS5 index."""
    global _db

    # Load files
    for path in sorted(_CONTENT_DIR.glob("*.md")):
        name = path.stem
        _sections[name] = path.read_text(encoding="utf-8")

    # Build FTS5 index
    _db = sqlite3.connect(":memory:", check_same_thread=False)
    _db.execute("CREATE VIRTUAL TABLE cv_fts USING fts5(section, content)")
    for name, content in _sections.items():
        _db.execute("INSERT INTO cv_fts(section, content) VALUES (?, ?)", (name, content))
    _db.commit()


def list_sections() -> list[dict]:
    """Return name and one-line description for each available section."""
    return [
        {"name": name, "description": desc}
        for name, desc in _SECTION_DESCRIPTIONS.items()
        if name in _sections
    ]


def get_section(name: str) -> str:
    """Return the full markdown content of a section. Raises KeyError if not found."""
    if name not in _sections:
        raise KeyError(f"Section '{name}' not found. Available: {list(_sections.keys())}")
    return _sections[name]


def search(query: str, top_k: int = 5) -> list[dict]:
    """Full-text search across all sections. Returns matches with snippets and scores.

    Score is the negated FTS5 rank (higher = more relevant).
    """
    cursor = _db.execute(
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
    # bm25() returns negative values (more negative = more relevant).
    # We negate so that higher = more relevant for consumers.
    return [
        {"section": row[0], "snippet": row[1], "score": -row[2]}
        for row in cursor.fetchall()
    ]


# Load content at import time.
_load()
