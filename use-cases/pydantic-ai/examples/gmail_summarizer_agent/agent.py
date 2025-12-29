"""
Agent orchestrator that reviews unread Gmail conversations and drafts replies.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import List, Optional

from pydantic_ai import Agent, RunContext

from .gmail_tool import GmailClient, run_in_background
from .models import BatchDraftSummary, DraftPlan
from .providers import get_llm_model
from .settings import settings

SYSTEM_PROMPT = """
Du bist ein fokussierter E-Mail-Triage-Agent für das Gmail-Konto {account_email}.

Arbeitsablauf:
1. Rufe zunächst mit dem Tool `fetch_open_emails` alle relevanten offenen/unbearbeiteten Nachrichten ab.
2. Analysiere jede Nachricht und fasse sie in 2-3 Stichpunkten zusammen.
3. Formuliere konkrete Antwortvorschläge. Wenn genug Kontext vorhanden ist, speichere die Antwort mit `save_reply_draft`.
4. Lege für jede Nachricht fest, ob eine Antwort vorbereitet wurde oder warum sie übersprungen wurde.

Richtlinien:
- Bleibe präzise, keine Marketingfloskeln.
- Nutze den existierenden Tonfall des Gegenübers.
- Wenn Informationen fehlen, markiere die Nachricht als „übersprungen“ und begründe dies.
- Antworte auf Deutsch, außer die ursprüngliche Mail ist klar in einer anderen Sprache.
- Gib im Ergebnis immer eine operator-orientierte Zusammenfassung zurück.
"""


@dataclass
class GmailAgentDependencies:
    """Dependencies injected into the agent at runtime."""

    gmail_client: GmailClient
    account_email: str
    max_messages: int = settings.gmail_max_messages


gmail_triage_agent = Agent(
    get_llm_model(),
    deps_type=GmailAgentDependencies,
    result_type=BatchDraftSummary,
    system_prompt=SYSTEM_PROMPT.format(account_email=settings.gmail_account_email),
)


@gmail_triage_agent.tool
async def fetch_open_emails(
    ctx: RunContext[GmailAgentDependencies],
    limit: Optional[int] = None,
) -> List[dict]:
    """
    Load unread inbox messages that still need follow-up.
    """
    max_results = limit or ctx.deps.max_messages
    messages = await run_in_background(ctx.deps.gmail_client.list_open_messages, max_results)
    return [message.model_dump() for message in messages]


@gmail_triage_agent.tool
async def save_reply_draft(
    ctx: RunContext[GmailAgentDependencies],
    draft: DraftPlan,
) -> dict:
    """
    Persist a reply draft in Gmail so the operator can review/send it later.
    """
    metadata = await run_in_background(
        ctx.deps.gmail_client.create_reply_draft,
        message_id=draft.message_id,
        thread_id=draft.thread_id,
        recipient=draft.recipient,
        subject=draft.subject,
        body=draft.body,
    )
    return metadata


async def triage_open_emails(
    *,
    instruction: Optional[str] = None,
    max_messages: Optional[int] = None,
) -> BatchDraftSummary:
    """
    Convenience wrapper used by the CLI / demos.
    """
    gmail_client = GmailClient(
        credentials_path=settings.gmail_credentials_path,
        token_path=settings.gmail_token_path,
        user_id=settings.gmail_user_id,
    )

    deps = GmailAgentDependencies(
        gmail_client=gmail_client,
        account_email=settings.gmail_account_email,
        max_messages=max_messages or settings.gmail_max_messages,
    )

    user_prompt = instruction or "Triage alle offenen Gmail-Nachrichten und bereite Antworten als Draft vor."
    result = await gmail_triage_agent.run(user_prompt, deps=deps)
    return result.data


def triage_sync(**kwargs) -> BatchDraftSummary:
    """Sync helper for environments where asyncio is not used."""
    return asyncio.run(triage_open_emails(**kwargs))


if __name__ == "__main__":
    summary = triage_sync()
    print("=== Gmail Draft Zusammenfassung ===")
    print(summary.model_dump_json(indent=2, ensure_ascii=False))
