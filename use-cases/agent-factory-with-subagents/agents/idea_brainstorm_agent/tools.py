"""Utility helpers and tools for repository-aware brainstorming."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

AGENT_ROOT = Path(__file__).resolve().parent


def _project_root() -> Path:
    """Attempt to locate the repository root by walking up until we find a .git folder."""

    for ancestor in AGENT_ROOT.parents:
        if (ancestor / ".git").exists():
            return ancestor
    # Fallback: assume the agent directory itself
    return AGENT_ROOT


REPO_ROOT = _project_root()


@dataclass
class FileSnippet:
    """Small slice of a repository file."""

    path: str
    content: str
    relevance: float


@dataclass
class IdeaDraft:
    """Intermediate representation before final JSON serialization."""

    title: str
    source_reference: str
    insight: str
    roi_signal: str
    next_step: str


def sample_repository_files(prompt: str, paths: Iterable[str], limit: int) -> List[FileSnippet]:
    """Return up to ``limit`` snippets ranked by keyword overlap."""

    keywords = _keywords(prompt)
    scored: List[FileSnippet] = []
    fallback: List[FileSnippet] = []

    for raw_path in paths:
        location = _resolve_path(raw_path)
        if location is None or not location.exists():
            continue
        location = location.resolve()

        candidate_files: List[Path]
        if location.is_dir():
            candidate_files = [
                *location.rglob("*.md"),
                *location.rglob("*.py"),
            ]
        else:
            candidate_files = [location]

        for file_path in candidate_files:
            file_path = file_path.resolve()
            if len(scored) >= limit * 4:  # lightweight safety valve
                break

            try:
                text = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            snippet = text.strip().replace("\r", "")[:1200]
            score = _score(snippet, keywords)
            if score == 0:
                if len(fallback) < limit:
                    fallback.append(
                        FileSnippet(
                            path=_relative_path(file_path),
                            content=snippet,
                            relevance=0.0,
                        )
                    )
                continue
            scored.append(
                FileSnippet(
                    path=_relative_path(file_path),
                    content=snippet,
                    relevance=score,
                )
            )

    if scored:
        scored.sort(key=lambda entry: entry.relevance, reverse=True)
        return scored[:limit]
    return fallback[:limit]


def snippets_to_context(snippets: Iterable[FileSnippet]) -> str:
    """Convert snippets into a compact context string for the LLM."""

    blocks = []
    for snippet in snippets:
        blocks.append(f"SOURCE: {snippet.path}\nCONTENT:\n{snippet.content}\n---")
    return "\n\n".join(blocks)


def classify_roi(impact: int, confidence: int, effort: int) -> str:
    """Lightweight ROI heuristic used by both the LLM and unit tests."""

    for value, label in ((impact, "impact"), (confidence, "confidence"), (effort, "effort")):
        if not 1 <= value <= 5:
            raise ValueError(f"{label} must be between 1 and 5")

    composite = (impact * 0.4) + (confidence * 0.4) - (effort * 0.3)
    if composite >= 2.0:
        return "High"
    if composite >= 1.0:
        return "Medium"
    return "Low"


def normalize_title(title: str) -> str:
    """Normalize whitespace and capitalization for idea titles."""

    cleaned = re.sub(r"\s+", " ", title or "").strip()
    return cleaned[:80].title() if cleaned else "Untitled Insight"


def _keywords(text: str) -> List[str]:
    return [token for token in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(token) > 3]


def _score(snippet: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.0
    lower_snippet = snippet.lower()
    hits = sum(lower_snippet.count(keyword) for keyword in keywords)
    return hits / (len(snippet) + 1)


def _resolve_path(raw_path: str) -> Optional[Path]:
    raw = raw_path.strip()
    candidate = Path(raw)
    possible = [candidate]
    if not candidate.is_absolute():
        possible.extend(
            [
                (Path.cwd() / candidate).resolve(strict=False),
                (AGENT_ROOT / candidate).resolve(strict=False),
                (REPO_ROOT / Path(_strip_leading_parent_refs(raw))).resolve(strict=False),
            ]
        )

    checked = set()
    for option in possible:
        try:
            key = option.resolve(strict=False)
        except RuntimeError:
            key = option
        if key in checked:
            continue
        checked.add(key)
        if option.exists():
            return option
    return None


def _relative_path(file_path: Path) -> str:
    try:
        return str(file_path.relative_to(REPO_ROOT))
    except ValueError:
        try:
            return str(file_path.relative_to(Path.cwd()))
        except ValueError:
            return str(file_path)


def _strip_leading_parent_refs(path_str: str) -> str:
    cleaned = path_str.lstrip("./")
    while cleaned.startswith("../"):
        cleaned = cleaned[3:]
    return cleaned or "."
