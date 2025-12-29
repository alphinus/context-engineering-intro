name: "Multi-Agent System: Ideen-Generator mit Strukturierungs-Sub-Agent"
description: |

## Zweck
Erstelle ein Pydantic-AI-Multi-Agent-System, bei dem ein primärer **Ideen-Generator-Agent** kreative Konzepte entwickelt und einen **Strukturierungs-Agent** als Tool verwendet.  
Dieser Sub-Agent hilft, die generierten Ideen zu ordnen, zu bewerten oder zu priorisieren.  
Das System demonstriert das Muster „Agent als Tool“ mit modularen Agent-Komponenten.

## Grundprinzipien
1. **Kontext ist entscheidend**: Alle relevanten Dokumente, Beispiele und Randbedingungen müssen integriert werden.
2. **Validierungsschleifen**: Jeder Agent sollte überprüfbare Tests und Selbstvalidierungen besitzen.
3. **Informationsdichte**: Hohe inhaltliche Präzision und semantische Wiedererkennbarkeit im Code.
4. **Progressive Verbesserung**: Start mit einfacher Logik, danach inkrementell erweitern.

---

## Ziel
Ein produktionsreifes Multi-Agent-System, das über eine CLI oder API Ideen generiert, strukturiert und präsentiert.  
Der Hauptagent erzeugt Ideen, während der Unteragent hilft, sie zu kategorisieren, bewerten oder in einem strukturierten Format (z. B. JSON, Markdown oder Tabelle) aufzubereiten.

## Warum
- **Wert**: Unterstützt Teams und Einzelpersonen beim systematischen Ideengenerieren.
- **Integration**: Demonstriert fortgeschrittene Pydantic-AI-Agenten-Muster.
- **Problem**: Übersetzt kreative, unstrukturierte Ideen in klare, umsetzbare Formate.

## Was
Ein CLI-basiertes System, in dem:
- Benutzer Themen oder Probleme eingeben
- Der Ideen-Agent generiert kreative Lösungen oder Konzepte
- Der Strukturierungs-Agent organisiert, bewertet oder priorisiert diese Ideen
- Ergebnisse werden in Echtzeit gestreamt und dokumentiert

### Erfolgskriterien
- [ ] Ideen-Agent generiert konsistente Ergebnisse auf Anfrage
- [ ] Strukturierungs-Agent erstellt strukturierte Ausgabeformate
- [ ] Hauptagent kann Sub-Agent korrekt aufrufen
- [ ] CLI zeigt Echtzeit-Feedback und Tool-Nutzung
- [ ] Alle Tests und Validierungen bestehen

## Erforderlicher Kontext

### Dokumentation & Referenzen
```yaml
- url: https://ai.pydantic.dev/agents/
  why: Grundlegende Agentenarchitektur

- url: https://ai.pydantic.dev/multi-agent-applications/
  why: Multi-Agent-Muster, besonders Agent-als-Tool

- file: examples/agent/agent.py
  why: Beispiel für Agent-Definition und Tool-Registrierung

- file: examples/cli.py
  why: Beispiel für CLI-Integration mit Streaming-Ausgabe
