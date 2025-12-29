"""
LLM provider utilities shared across the Gmail agent modules.
"""

from __future__ import annotations

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from .settings import settings


def get_llm_model() -> OpenAIModel:
    """Return a configured OpenAI-compatible model using repository settings."""
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
    )
    return OpenAIModel(settings.llm_model, provider=provider)
