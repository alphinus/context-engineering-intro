# Gmail Summarizer Agent

Ein Pydantic-AI-Agent, der alle offenen Gmail-Nachrichten des Posteingangs `alphinus@gmai.com` (oder eines beliebigen Kontos) abruft, zusammenfasst und automatisch Antwortentwürfe als Draft speichert. Die Idee: Du überfliegst nur noch die generierten Drafts und klickst anschließend auf **Senden**.

## Funktionsumfang

- Liest ungelesene/noch unbeantwortete Nachrichten aus dem Gmail-Posteingang
- Analysiert Inhalt, Absender, Tonalität und erforderliche Aktionen
- Erstellt prägnante Zusammenfassungen pro Nachricht
- Schreibt Antwortvorschläge im passenden Stil und legt sie als Gmail-Draft ab
- Gibt am Ende eine strukturierte Übersicht (`BatchDraftSummary`) zurück

## Setup

```bash
cd use-cases/pydantic-ai/examples/gmail_summarizer_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1. LLM-Konfiguration (.env)

Lege im Repository eine `.env` an (oder erweitere die bestehende) und definiere:

```env
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini        # optional anpassen
LLM_BASE_URL=https://api.openai.com/v1
GMAIL_CREDENTIALS_PATH=credentials/credentials.json
GMAIL_TOKEN_PATH=credentials/token.json
GMAIL_USER_ID=me             # bleibt meist 'me'
GMAIL_ACCOUNT_EMAIL=alphinus@gmai.com
GMAIL_MAX_MESSAGES=5         # wie viele offene Threads der Agent bearbeiten soll
```

> Tipp: Unter `use-cases/pydantic-ai/examples/gmail_summarizer_agent/example.env` findest du eine ausfüllbare Vorlage, die du nur noch kopieren und mit echten Werten ersetzen musst.

### 2. Gmail OAuth vorbereiten

1. Erstelle in der [Google Cloud Console](https://console.cloud.google.com/apis/credentials) ein OAuth2-Client (Desktop-App).
2. Lade die `credentials.json` herunter und speichere sie unter `use-cases/pydantic-ai/examples/gmail_summarizer_agent/credentials/credentials.json`.
3. Beim ersten Start öffnet sich ein Browserfenster für den OAuth-Flow. Danach liegt das Token unter `credentials/token.json`.

Die benötigten Scopes sind bereits im Code hinterlegt (`gmail.readonly`, `gmail.modify`, `gmail.compose`, `gmail.metadata`).

## Agent ausführen

```bash
python agent.py
```

oder innerhalb eines anderen Skripts:

```python
from gmail_summarizer_agent.agent import triage_sync

summary = triage_sync(max_messages=10)
print(summary)
```

Der Agent ruft automatisch `fetch_open_emails`, bewertet jede Nachricht und speichert – sofern sinnvoll – Antwortentwürfe via `save_reply_draft`. Die Ausgabe enthält alle Draft-IDs, sodass du sie direkt in Gmail öffnen kannst.

## Tipps

- Passe `GMAIL_MAX_MESSAGES` an, wenn du viele offene Threads hast.
- Falls du mehrere Konten betreust, kannst du für jedes Konto eine eigene `.env` + Credentials verwenden.
- Für lokale Tests ohne echtes Gmail kannst du `LLM_API_KEY` auf einen Dummy-Wert setzen. Die Gmail-Calls benötigen jedoch echte OAuth-Daten.
