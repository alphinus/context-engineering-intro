# Idea Brainstorm Agent - INITIAL

## Feature
Build a Pydantic AI agent that reviews the existing `examples/` and `use-cases/` documentation in this repository, brainstorms fresh product or feature ideas, and produces JSON-formatted improvement proposals. Each proposal must summarize the referenced asset, explain the opportunity, and recommend next steps.

## Requirements
- Accept a topic prompt plus optional file paths to prioritize.
- Scan curated folders (`examples/`, `use-cases/`, `CLAUDE.md`, `INITIAL.md`) to collect context snippets.
- Generate 3-5 structured idea entries including: `title`, `source_reference`, `insight`, `roi_signal`, `next_step`.
- Highlight trend analysis (market/ROI) using predefined reasoning helpers.
- Return machine-consumable JSON with deterministic schema.

## Constraints
- Keep runtime under 2 minutes; avoid loading entire folders when only a few files are needed.
- Never fabricate sources; include relative paths for every recommendation.
- Use Anthropic Claude (default) with fallback to OpenAI GPT-4o; no external network calls beyond repository content.

## Validation
- Unit tests covering: parsing inputs, summarizing sample docs, generating structured output, handling empty matches.
- CLI command `poetry run python agent.py --prompt "Need onboarding ideas" --paths examples/` must emit JSON and exit 0.
