"""
Lightweight Gmail helper that lists unread emails and saves reply drafts.
"""

from __future__ import annotations

import asyncio
import base64
import logging
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import GmailMessage
from .settings import settings

logger = logging.getLogger(__name__)


class GmailClient:
    """Wrapper around the Gmail API that focuses on unread threads + drafts."""

    def __init__(
        self,
        credentials_path: Path,
        token_path: Path,
        user_id: str,
        scopes: Optional[List[str]] = None,
    ) -> None:
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.user_id = user_id
        self.scopes = scopes or settings.gmail_scopes
        self._creds: Optional[Credentials] = None
        self._service = None

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------
    def list_open_messages(self, max_results: int = 5) -> List[GmailMessage]:
        """
        Return unread inbox messages as lightweight Pydantic models.

        Args:
            max_results: Limit applied to the Gmail API query (1-20)
        """
        service = self._get_service()
        max_results = min(max(max_results, 1), 20)

        try:
            response = (
                service.users()
                .messages()
                .list(
                    userId=self.user_id,
                    labelIds=["INBOX", "UNREAD"],
                    maxResults=max_results,
                )
                .execute()
            )
        except HttpError as exc:
            logger.error("Unable to list Gmail messages: %s", exc)
            raise

        message_ids = [item["id"] for item in response.get("messages", [])]
        messages: List[GmailMessage] = []
        for msg_id in message_ids:
            message = self._fetch_message(msg_id)
            if message:
                messages.append(message)

        return messages

    def create_reply_draft(
        self,
        *,
        message_id: str,
        thread_id: str,
        recipient: str,
        subject: str,
        body: str,
    ) -> Dict[str, str]:
        """
        Store a Gmail draft that replies to the given message.
        """
        if not recipient:
            raise ValueError("Recipient email is required to create a draft")

        service = self._get_service()

        mime_message = MIMEText(body)
        mime_message["To"] = recipient
        mime_message["Subject"] = subject
        mime_message["In-Reply-To"] = message_id
        mime_message["References"] = message_id

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        try:
            draft = (
                service.users()
                .drafts()
                .create(
                    userId=self.user_id,
                    body={"message": {"raw": encoded_message, "threadId": thread_id}},
                )
                .execute()
            )
        except HttpError as exc:
            logger.error("Failed to save Gmail draft: %s", exc)
            raise

        logger.info("Draft %s created for thread %s", draft.get("id"), thread_id)

        return {
            "draft_id": draft.get("id", ""),
            "message_id": message_id,
            "thread_id": draft.get("message", {}).get("threadId", thread_id),
            "recipient": recipient,
            "subject": subject,
        }

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------
    def _get_service(self):
        """Build (or reuse) the Gmail discovery client."""
        if self._service is None:
            self._service = build("gmail", "v1", credentials=self._get_credentials(), cache_discovery=False)
        return self._service

    def _get_credentials(self) -> Credentials:
        """
        Ensure valid OAuth credentials exist.

        Follows Google's quickstart pattern but writes to the configured token path.
        """
        if self._creds and self._creds.valid:
            return self._creds

        if self.token_path.exists():
            self._creds = Credentials.from_authorized_user_file(
                str(self.token_path),
                scopes=self.scopes,
            )

        if self._creds and self._creds.expired and self._creds.refresh_token:
            self._creds.refresh(Request())
        elif not self._creds:
            if not self.credentials_path.exists():
                raise FileNotFoundError(
                    f"Gmail credentials not found at {self.credentials_path}. "
                    "Download OAuth client credentials from Google Cloud and try again."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.credentials_path),
                self.scopes,
            )
            # Browser-based OAuth flow; this blocks until the user authenticates
            self._creds = flow.run_local_server(port=0)

        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_path.write_text(self._creds.to_json(), encoding="utf-8")

        return self._creds

    def _fetch_message(self, message_id: str) -> Optional[GmailMessage]:
        """Return a rich GmailMessage if fetching succeeds."""
        service = self._get_service()

        try:
            data = (
                service.users()
                .messages()
                .get(userId=self.user_id, id=message_id, format="full")
                .execute()
            )
        except HttpError as exc:
            logger.warning("Unable to fetch message %s: %s", message_id, exc)
            return None

        headers = {h["name"].lower(): h["value"] for h in data.get("payload", {}).get("headers", [])}

        subject = headers.get("subject", "(Kein Betreff)")
        sender_raw = headers.get("from", "")
        sender_name, sender_email = parseaddr(sender_raw)
        reply_to = headers.get("reply-to", sender_email or sender_raw)
        timestamp = headers.get("date")
        received_at = parsedate_to_datetime(timestamp) if timestamp else None
        if received_at is None:
            received_at = datetime.now(timezone.utc)

        body_text = self._extract_body_text(data.get("payload", {})) or data.get("snippet", "")
        sender_display = sender_name or sender_email or sender_raw or "Unbekannter Kontakt"
        reply_target = reply_to or sender_email or sender_raw or ""

        return GmailMessage(
            id=data.get("id", message_id),
            thread_id=data.get("threadId", ""),
            subject=subject,
            sender=sender_display,
            received_at=received_at,
            snippet=data.get("snippet", ""),
            body_text=body_text,
            reply_to=reply_target,
        )

    def _extract_body_text(self, payload: Dict) -> str:
        """Attempt to capture a plaintext body from the Gmail payload tree."""

        def _decode(part: Dict) -> str:
            data = part.get("body", {}).get("data")
            if not data:
                return ""
            decoded = base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="ignore")
            return decoded

        mime_type = payload.get("mimeType", "")
        if mime_type == "text/plain":
            return _decode(payload)

        parts = payload.get("parts", []) or []
        for part in parts:
            if part.get("mimeType") == "text/plain":
                text = _decode(part)
                if text.strip():
                    return text

        # Nested structures (multipart/alternative -> parts -> text/plain)
        for part in parts:
            nested = part.get("parts")
            if nested:
                for sub_part in nested:
                    if sub_part.get("mimeType") == "text/plain":
                        text = _decode(sub_part)
                        if text.strip():
                            return text

        return ""


async def run_in_background(func, *args, **kwargs):
    """Utility that offloads blocking Gmail operations to a thread."""
    return await asyncio.to_thread(func, *args, **kwargs)
