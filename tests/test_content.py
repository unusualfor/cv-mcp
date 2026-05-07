"""Tests for the cv_mcp content layer."""

import pytest

from cv_mcp import content

EXPECTED_SECTIONS = {"profile", "experience", "work", "tech", "narrative"}


def test_all_sections_load():
    """All five sections are discovered and listed."""
    sections = content.list_sections()
    names = {s["name"] for s in sections}
    assert names == EXPECTED_SECTIONS
    assert len(sections) == 5
    # Each entry has name and description
    for s in sections:
        assert "name" in s
        assert "description" in s
        assert len(s["description"]) > 0


def test_get_section_returns_content():
    """Each known section returns non-empty markdown content."""
    for name in EXPECTED_SECTIONS:
        text = content.get_section(name)
        assert isinstance(text, str)
        assert len(text) > 100  # Each file should have substantial content


def test_get_section_unknown_raises():
    """Requesting a non-existent section raises KeyError."""
    with pytest.raises(KeyError):
        content.get_section("nonexistent")


def test_search_returns_match():
    """Searching for a term known to be in the content returns results."""
    results = content.search("Cisco")
    assert len(results) >= 1
    for r in results:
        assert "section" in r
        assert "snippet" in r
        assert "score" in r
        assert r["section"] in EXPECTED_SECTIONS
        assert len(r["snippet"]) > 0
        assert r["score"] >= 0
