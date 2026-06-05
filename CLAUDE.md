# WebDesign Honeyapps — Arbeitsbereich

## Zweck
Dieser Ordner dient als zentraler Arbeitsbereich für die Erstellung von Websites für verschiedene Unternehmen (Kunden). Jedes Unternehmen hat seinen eigenen Unterordner mit eigenem Git-Repository.

## Ordnerstruktur

```
WebDesign_Honeyapps/
├── CLAUDE.md               # Diese Datei
├── .agents/                # Installierte Skills (nicht bearbeiten)
└── <UnternehmenName>/      # Ein Ordner pro Kunde/Website
    ├── .git/
    ├── CLAUDE.md           # Kunden-spezifische Anweisungen
    └── ...                 # Website-Dateien
```

## Workflow: Neue Website anlegen

Wenn du eine neue Website für ein Unternehmen erstellst, halte dich an folgende Schritte:

1. Neuen Ordner anlegen: `mkdir <UnternehmenName>`
2. Git-Repository initialisieren: `cd <UnternehmenName> && git init`
3. Remote-Repository auf GitHub erstellen und verknüpfen
4. Kunden-CLAUDE.md mit projekt-spezifischen Infos anlegen
5. Website entwickeln

## Namenskonvention

- Ordner- und Repo-Namen: `kebab-case` (z.B. `mueller-gmbh`, `becker-architekten`)
- Verwende beschreibende Namen, die das Unternehmen eindeutig identifizieren

## Verfügbare Skills

Installiert via `npx skills add anthropics/skills`:

- **frontend-design** — UI-Komponenten und Frontend-Entwicklung
- **canvas-design** — Canvas-basierte Grafiken und Animationen
- **brand-guidelines** — Markenrichtlinien und Corporate Design
- **theme-factory** — Theme-Erstellung und Design-Systeme
- **web-artifacts-builder** — Web-App Erstellung
- **webapp-testing** — Webapp-Tests
- **claude-api** — Claude API Integration
- und weitere (siehe `.agents/skills/`)
