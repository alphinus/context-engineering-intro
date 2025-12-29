"""Settings module for the Idea Brainstorm Agent."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env early so BaseSettings can pick up overrides
load_dotenv()


class Settings(BaseSettings):
    """Environment-driven configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    anthropic_api_key: str | None = Field(
        default=None,
        alias="ANTHROPIC_API_KEY",
        description="Primary API key for Claude models.",
    )
    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
        description="Fallback API key for OpenAI-compatible providers.",
    )
    model: str = Field(
        default="claude-3-5-sonnet-20241022",
        alias="IDEA_AGENT_MODEL",
        description="Default model used for brainstorming.",
    )
    fallback_model: str = Field(
        default="gpt-4o-mini",
        alias="IDEA_AGENT_FALLBACK_MODEL",
        description="Model used when the primary provider is unavailable.",
    )
    provider: str = Field(
        default="anthropic",
        alias="IDEA_AGENT_PROVIDER",
        description="Force a specific provider ('anthropic' or 'openai').",
    )
    max_sampled_files: int = Field(
        default=5,
        alias="MAX_SAMPLED_FILES",
        ge=1,
        le=15,
        description="Upper bound on how many files can be sampled per run.",
    )
    default_search_paths: str = Field(
        default="examples,use-cases,CLAUDE.md,INITIAL.md",
        alias="DEFAULT_SEARCH_PATHS",
        description="Comma-separated list of repositories to crawl when no paths provided.",
    )

    def resolved_search_paths(self) -> List[str]:
        """Return the default search paths as a clean list."""

        return [segment.strip() for segment in self.default_search_paths.split(",") if segment.strip()]

    def preferred_provider(self) -> str:
        """Return the explicitly requested provider, normalized."""

        return (self.provider or "anthropic").strip().lower()


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    """Load and cache settings once per process."""

    return Settings()  # type: ignore[call-arg]


settings = load_settings()
