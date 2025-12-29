"""Command-line entry point for the Idea Brainstorm Agent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from rich.console import Console

from .agent import IdeaGenerationResult, brainstorm
from .providers import provider_summary
from .settings import settings

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repository-aware brainstorming agent")
    parser.add_argument(
        "--prompt",
        required=True,
        help="Topic or question for idea generation",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="Optional list of directories/files to prioritize",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=0,
        help="Maximum files to sample (defaults to settings)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    search_paths: List[str] = []
    if args.paths:
        for raw in args.paths:
            path = Path(raw)
            search_paths.append(str(path))

    console.print("[bold cyan]Idea Brainstorm Agent[/bold cyan]")
    console.print(f"Using provider: {provider_summary()}")

    result: IdeaGenerationResult = brainstorm(
        prompt=args.prompt,
        paths=search_paths or None,
        max_files=args.max_files,
    )

    console.print("\n[bold]JSON Output[/bold]")
    console.print_json(result.model_dump_json(indent=2))
    console.print("\n[green]Done[/green]")


if __name__ == "__main__":
    main()
