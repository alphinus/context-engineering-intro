# Tools Plan

## FileSamplerTool
- Inputs: `paths: List[str]`, `limit: int` (default 5)
- Behavior: Walk whitelisted directories, pick the most relevant files (keyword match on prompt), return snippets + metadata.
- Used by: `trend_analyst` helper.

## IdeaFormatter
- Inputs: `raw_ideas: List[IdeaDraft]`
- Behavior: Validate titles, attach ROI classification (High/Medium/Low) using heuristics (market size vs. effort), deduplicate.
- Used before final response to enforce JSON schema.

## ROIHeuristics
- Pure function returning ROI signal from `impact`, `confidence`, `effort` integers.
- Shared by both main agent and unit tests.
