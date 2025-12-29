"""LLM provider configuration for the Idea Brainstorm Agent."""

from __future__ import annotations

from typing import Optional

from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.openai import OpenAIProvider

from .settings import settings


def get_llm_model(model_choice: Optional[str] = None):
    """Return a configured Anthropic (preferred) or OpenAI-compatible model."""

    preferred = settings.preferred_provider()

    if preferred == "anthropic" and settings.anthropic_api_key:
        provider = AnthropicProvider(api_key=settings.anthropic_api_key)
        return AnthropicModel(model_choice or settings.model, provider=provider)

    if settings.openai_api_key:
        provider = OpenAIProvider(api_key=settings.openai_api_key)
        return OpenAIModel(model_choice or settings.fallback_model, provider=provider)

    raise RuntimeError("Missing API keys. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your environment.")


def provider_summary() -> dict:
    """Expose current provider information for debugging and telemetry."""

    preferred = settings.preferred_provider()
    if preferred == "anthropic" and settings.anthropic_api_key:
        active_provider = "anthropic"
        model = settings.model
    elif settings.openai_api_key:
        active_provider = "openai"
        model = settings.fallback_model
    else:
        active_provider = "unknown"
        model = "n/a"

    return {
        "provider": active_provider,
        "model": model,
        "max_sampled_files": settings.max_sampled_files,
    }
