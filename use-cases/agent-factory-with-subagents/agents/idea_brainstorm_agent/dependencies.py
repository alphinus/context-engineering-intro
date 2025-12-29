"""Dependencies injected into the Idea Brainstorm Agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .settings import Settings, settings


@dataclass
class AgentDependencies:
    """Runtime dependencies and request context."""

    prompt: str
    search_paths: List[str] = field(default_factory=list)
    max_files: int = field(default=0)
    settings: Settings = field(default=settings)

    def resolved_paths(self) -> List[str]:
        """Return caller-provided paths or fall back to defaults."""

        return self.search_paths or self.settings.resolved_search_paths()

    def resolved_limit(self) -> int:
        """Return caller max_files or default from settings."""

        return self.max_files or self.settings.max_sampled_files
