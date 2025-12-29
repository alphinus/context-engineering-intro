🔄 Projektbewusstsein & Kontext

Lies immer PLANNING.md zu Beginn einer neuen Session, um den Zweck, den Aufbau und die Denkmuster des Ideen-Generators zu verstehen.

Überprüfe TASK.md, bevor du eine neue Idee oder Forschungsrichtung beginnst. Wenn sie fehlt, füge sie mit kurzer Beschreibung und Datum hinzu.

Halte Namenskonventionen und Datei-Struktur wie in PLANNING.md beschrieben konsequent ein.

Nutze venv_linux (die virtuelle Umgebung) bei allen Python-Befehlen, falls der Agent Erweiterungen ausführt (z. B. API-Aufrufe, Wissenssuche).

🧱 Struktur & Modularität

Keine Datei über 500 Zeilen. Bei wachsendem Umfang: Aufteilen in Module oder thematische Dateien.

Organisiere den Code nach logischen Funktionen:

idea_agent.py – zentrale Logik zur Ideengenerierung

research_tool.py – Recherche-Tool oder API-Anbindung

prompt_templates.py – System- und Promptvorlagen

Verwende konsistente Imports und python_dotenv für Umgebungsvariablen.

🧪 Qualität & Zuverlässigkeit

Erstelle Tests, die sicherstellen, dass der Agent valide, strukturierte Ideen zurückgibt.

Bei Änderungen der Logik: bestehende Tests prüfen und ggf. anpassen.

Tests liegen im Ordner /tests mit mindestens:

1 Test für erwartete Idee (z. B. kreative, aber realistische Vorschläge)

1 Grenzfall (z. B. unklare Prompts)

1 Fehlerfall (z. B. fehlende Daten oder API-Fehler).

✅ Aufgabenverfolgung

Markiere abgeschlossene Aufgaben in TASK.md, sobald ein Teilprozess (z. B. „Ideensammlung“, „Clustering“, „Bewertung“) abgeschlossen ist.

Neue Unteraufgaben oder Erkenntnisse während des Arbeitens unter „Entdeckt während der Arbeit“ hinzufügen.

📎 Stil & Konventionen

Primäre Sprache: Python.

Einhalten von PEP8, Typannotationen und Formatierung mit black.

Datenvalidierung mit pydantic, wenn der Agent Ideen strukturiert ausgibt (z. B. als JSON).

Dokumentiere jede Funktion nach Google-Style:

def generate_idea(prompt: str) -> dict:
    """
    Generiert eine neue Idee basierend auf einem Prompt.

    Args:
        prompt (str): Beschreibung oder Kontext für die Ideengenerierung.

    Returns:
        dict: Strukturierte Idee mit Titel, Beschreibung, möglichen nächsten Schritten.
    """

📚 Dokumentation & Verständlichkeit

README.md regelmäßig aktualisieren, wenn neue Module, APIs oder Inspirationsquellen ergänzt werden.

Nicht offensichtliche Logik kommentieren.

Bei komplexen Heuristiken Inline-Kommentare mit # Reason: hinzufügen, um das Warum zu erklären.

🧠 KI-Verhaltensregeln

Nie Kontext annehmen – bei Unklarheit nachfragen.

Keine Halluzinationen oder erfundenen Quellen. Nur bekannte, überprüfbare APIs oder Wissensquellen verwenden.

Dateipfade und Modulnamen vor Nutzung prüfen.

Kein Überschreiben bestehender Dateien, außer dies ist ausdrücklich in TASK.md vorgesehen.