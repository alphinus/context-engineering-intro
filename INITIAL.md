## FEATURE:

* Ein Pydantic-AI-Agent, der Ideen generiert und strukturiert.
* Der Hauptagent ist ein „Ideen-Agent“, der einen zweiten Agenten („Recherche-Agent“) als Tool verwendet, um relevante Informationen oder Inspirationen zu sammeln.
* Eine optionale CLI ermöglicht es, den Agenten direkt mit Prompts zu steuern.
* Der Recherche-Agent nutzt z. B. die Brave API oder eine interne Wissensdatenbank zur Kontextsuche.

## EXAMPLES:

Im Ordner `examples/` befindet sich eine README-Datei, die erklärt, wie die Beispiele aufgebaut sind und wie du deine eigene Dokumentation strukturieren kannst.

* `examples/cli.py` – als Vorlage für die Erstellung der CLI
* `examples/agent/` – enthält Best-Practice-Beispiele für den Aufbau von Pydantic-AI-Agenten, die verschiedene LLMs und Provider unterstützen, Abhängigkeiten zwischen Agenten verwalten und Tools hinzufügen.

Diese Beispiele sollen nur als Orientierung dienen. Kopiere sie **nicht direkt**, da sie für ein anderes Projekt erstellt wurden. Verwende sie stattdessen als Inspiration und Referenz für Best Practices.

## DOCUMENTATION:

Pydantic AI Dokumentation: [https://ai.pydantic.dev/](https://ai.pydantic.dev/)

## OTHER CONSIDERATIONS:

* Eine Datei `.env.example` und ein README mit Setup-Anleitung müssen enthalten sein (inklusive Konfiguration des Recherche-Agents und API-Schlüssel).
* Die Projektstruktur soll im README erklärt werden.
* Eine virtuelle Umgebung mit allen Abhängigkeiten ist bereits vorbereitet.
* Verwende `python_dotenv` und `load_env()` zur Verwaltung der Umgebungsvariablen.
