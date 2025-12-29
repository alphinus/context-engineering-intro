"""Unit tests for ROI heuristics and file sampling."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools import classify_roi, sample_repository_files  # noqa: E402


FIXTURE_DOC = PROJECT_ROOT / "documents" / "sample_ideas.md"


def test_classify_roi_ranges() -> None:
    assert classify_roi(impact=5, confidence=5, effort=1) == "High"
    assert classify_roi(impact=3, confidence=3, effort=3) == "Medium"
    assert classify_roi(impact=2, confidence=2, effort=5) == "Low"


@pytest.mark.parametrize("invalid", [0, 6])
def test_classify_roi_validates_input(invalid: int) -> None:
    with pytest.raises(ValueError):
        classify_roi(impact=invalid, confidence=3, effort=2)


def test_sample_repository_files_limits(tmp_path: Path) -> None:
    target = tmp_path / "notes.md"
    target.write_text(FIXTURE_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    snippets = sample_repository_files(
        prompt="onboarding improvements",
        paths=[str(target)],
        limit=2,
    )
    assert len(snippets) <= 2
    assert any("onboarding" in snippet.content.lower() for snippet in snippets)
