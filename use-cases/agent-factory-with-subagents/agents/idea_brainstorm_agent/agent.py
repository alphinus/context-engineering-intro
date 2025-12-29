"""Primary Idea Brainstorm Agent implementation."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from .dependencies import AgentDependencies
from .prompts import MAIN_SYSTEM_PROMPT
from .providers import get_llm_model
from .tools import classify_roi, sample_repository_files, snippets_to_context


class Idea(BaseModel):
    """Structured output for a single idea."""

    title: str = Field(..., description="Short title for the idea")
    source_reference: str = Field(..., description="Relative file path that inspired the idea")
    insight: str = Field(..., description="Key observation or opportunity discovered")
    roi_signal: str = Field(..., pattern="^(High|Medium|Low)$", description="ROI classification")
    next_step: str = Field(..., description="Recommended follow-up action")


class IdeaGenerationResult(BaseModel):
    """Validated JSON response returned by the agent."""

    ideas: List[Idea] = Field(default_factory=list)
    trend_summary: str = Field(..., description="Short explanation of observed trends")
    inputs: dict = Field(default_factory=dict, description="Echo back prompt + paths")


idea_agent = Agent(
    get_llm_model(),
    deps_type=AgentDependencies,
    output_type=IdeaGenerationResult,
    system_prompt=MAIN_SYSTEM_PROMPT,
)


@idea_agent.tool
def sample_context(ctx: RunContext[AgentDependencies], limit: Optional[int] = None) -> str:
    """Collect repository snippets for the LLM."""

    snippets = sample_repository_files(
        prompt=ctx.deps.prompt,
        paths=ctx.deps.resolved_paths(),
        limit=limit or ctx.deps.resolved_limit(),
    )
    # Log via stdout to avoid dependency on context-specific logger attributes.
    print(f"[idea_brainstorm_agent] sampled {len(snippets)} files")
    return snippets_to_context(snippets)


@idea_agent.tool
def roi_helper(_: RunContext[AgentDependencies], impact: int, confidence: int, effort: int) -> str:
    """Expose the deterministic ROI heuristic to the LLM."""

    return classify_roi(impact, confidence, effort)


async def brainstorm_async(prompt: str, paths: Optional[List[str]] = None, max_files: int = 0) -> IdeaGenerationResult:
    """Async helper for direct library use."""

    deps = AgentDependencies(prompt=prompt, search_paths=paths or [], max_files=max_files)
    result = await idea_agent.run(prompt, deps=deps)
    return result.output


def brainstorm(prompt: str, paths: Optional[List[str]] = None, max_files: int = 0) -> IdeaGenerationResult:
    """Sync helper used by the CLI and tests."""

    deps = AgentDependencies(prompt=prompt, search_paths=paths or [], max_files=max_files)
    result = idea_agent.run_sync(prompt, deps=deps)
    return result.output
