# 💡 Idea Brainstorm Agent

An ideation-focused Pydantic AI agent that scans the repository's examples and documentation, performs mini market and ROI analysis, and outputs JSON-formatted improvement proposals. Use it to uncover quick wins hidden in the existing Context Engineering materials.

## Features
- Repository-aware brainstorming with explicit file citations
- Built-in helper personas (trend analyst, market researcher, ROI modeler)
- Deterministic JSON output validated by Pydantic models
- CLI flags for prompt, search paths, model override, and max files

## Quick Start
```bash
cd use-cases/agent-factory-with-subagents/agents/idea_brainstorm_agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API keys
python cli.py --prompt "Improve onboarding" --paths examples use-cases
```

## Environment
| Variable | Description |
| --- | --- |
| `ANTHROPIC_API_KEY` | Primary key for Claude models |
| `OPENAI_API_KEY` | Optional fallback for OpenAI-compatible models |
| `IDEA_AGENT_MODEL` | Override default Claude model name |
| `IDEA_AGENT_FALLBACK_MODEL` | Override fallback OpenAI model |

## Tests
```bash
pytest
```

## Output Schema
```json
{
  "ideas": [
    {
      "title": "string",
      "source_reference": "path/to/file.md",
      "insight": "string",
      "roi_signal": "High | Medium | Low",
      "next_step": "string"
    }
  ],
  "trend_summary": "string",
  "inputs": {
    "prompt": "string",
    "paths": ["examples", "use-cases"],
    "sampled_files": 3
  }
}
```
