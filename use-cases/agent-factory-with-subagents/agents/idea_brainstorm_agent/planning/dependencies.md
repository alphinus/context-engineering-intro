# Dependencies Plan

## Python
- Python 3.11
- Poetry for dependency management (align with repo standards)
- `pydantic-ai`, `python-dotenv`, `rich`

## Environment Variables
- `ANTHROPIC_API_KEY` (required)
- `OPENAI_API_KEY` (optional fallback)

## Data
- Relies on repository files only; ensure read permissions for `examples/`, `use-cases/`, `CLAUDE.md`, `INITIAL.md`.

## CLI
- Entry via `cli.py` exposing `--prompt`, `--paths`, `--model` flags.

## Testing
- Pytest with fixtures referencing sample documents under `documents/`.
