"""
Structured outputs used by the Gmail summarizer agent.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GmailMessage(BaseModel):
    """Minimal representation of a Gmail message the tools return."""

    id: str = Field(..., description="Gmail message ID")
    thread_id: str = Field(..., description="Thread identifier")
    subject: str = Field(default="(Kein Betreff)", description="Subject line")
    sender: str = Field(..., description="Person who sent the email")
    received_at: datetime = Field(..., description="Timestamp from the Date header")
    snippet: str = Field(..., description="Short excerpt provided by Gmail")
    body_text: str = Field(..., description="Plain-text version of the email body")
    reply_to: str = Field(..., description="Email address used for replying")


class DraftPlan(BaseModel):
    """Input the LLM uses when asking the Gmail tool to create a draft."""

    message_id: str = Field(..., description="Original message ID")
    thread_id: str = Field(..., description="Thread to keep conversation grouped")
    recipient: str = Field(..., description="Who should receive the draft reply")
    subject: str = Field(..., description="Subject line for the reply")
    body: str = Field(..., min_length=20, description="Full email body that should be saved")


class DraftOutcome(BaseModel):
    """Metadata returned after the Gmail tool stores a draft."""

    message_id: str = Field(..., description="Original Gmail message ID")
    draft_id: str = Field(..., description="Draft ID returned by Gmail")
    thread_id: str = Field(..., description="Thread ID for the draft")
    subject: str = Field(..., description="Subject submitted to Gmail")
    recipient: str = Field(..., description="Recipient email address")
    summary: str = Field(..., description="Short synopsis of the reply")


class BatchDraftSummary(BaseModel):
    """Structured result returned by the agent back to the CLI."""

    account: str = Field(..., description="Gmail account that was triaged")
    total_open_messages: int = Field(..., ge=0, description="How many emails were inspected")
    drafts_created: List[DraftOutcome] = Field(
        default_factory=list,
        description="Drafts generated during the run",
    )
    skipped_messages: Optional[List[str]] = Field(
        default=None,
        description="IDs for emails that were skipped (e.g., missing context)",
    )
    summary_notes: str = Field(..., description="High-level overview for the operator")
