"""
Environment-aware settings for the Gmail summarizer agent.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar, List

from dotenv import load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load env vars from repository root if present
load_dotenv()


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM configuration
    llm_provider: str = Field(default="openai", description="Provider identifier")
    llm_api_key: str = Field(..., description="API key compatible with the chosen provider")
    llm_model: str = Field(default="gpt-4o-mini", description="Model name to invoke")
    llm_base_url: str = Field(default="https://api.openai.com/v1")

    # Gmail configuration
    gmail_credentials_path: Path = Field(
        default=Path("credentials/credentials.json"),
        description="Path to OAuth client credentials (downloaded from Google Cloud)",
    )
    gmail_token_path: Path = Field(
        default=Path("credentials/token.json"),
        description="Path where the OAuth token will be stored after the flow runs once",
    )
    gmail_user_id: str = Field(
        default="me",
        description="Identifier passed to the Gmail API (usually 'me').",
    )
    gmail_account_email: str = Field(
        default="alphinus@gmai.com",
        description="Human-friendly label for the account being triaged.",
    )
    gmail_max_messages: int = Field(
        default=5,
        ge=1,
        le=20,
        description="How many open emails to summarize per run",
    )

    # OAuth scopes required for reading inbox + drafting replies
    gmail_scopes: ClassVar[List[str]] = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/gmail.metadata",
    ]


def load_settings() -> Settings:
    """
    Helper that returns a configured Settings instance.

    Falls back to dummy values so tests or docs can import the module
    without a fully configured environment.
    """
    try:
        return Settings()
    except ValidationError:
        os.environ.setdefault("LLM_API_KEY", "test-key")
        os.environ.setdefault("LLM_MODEL", "gpt-4o-mini")
        return Settings()


settings = load_settings()
