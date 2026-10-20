# Claude Code – Installation und Verwendung

Offizielle Dokumentation: https://code.claude.com/docs/en/skills (geprüft 2026-10-20).

- Claude Code **nutzt Verzeichnisse**, keine ZIP direkt als ausführbares Plugin: ZIP entpacken und den enthaltenen Ordner `conversion-psychology-web-builder` nach `<projekt>/.claude/skills/` (nur dieses Projekt) oder `~/.claude/skills/` (alle Projekte) kopieren.
- Aufruf im Claude Code Chat: `/conversion-psychology-web-builder` oder eine inhaltlich passende Website-Anfrage. Ob der Skill automatisch gewählt wird, hängt vom Kontext ab; bei wichtigen Projekten explizit aufrufen.
- Nur `SKILL.md` ist erforderlich, `references/` lädt Claude bei Bedarf nach; `agents/openai.yaml` dient ausschließlich der project-internen Portabilitätsstruktur und wird **nicht** als Claude-Code-Konfiguration benötigt.
- Python 3 ist **nur** für optionale Validierungsskripte nötig, nicht zum Laden von `SKILL.md`.
- Skills gewähren keine zusätzlichen Rechte: Dateizugriff, Browser, Tests und Deployment hängen von bestehender Claude-Code-Umgebung und Benutzerfreigaben ab.
- Änderungen in Kundencode erfolgen nur gemäß konkretem Auftrag. Vor unautorisierten Produktivänderungen, Analytics und Versand explizit Freigabe einholen.

## Optionaler Browser-Adapter
Der Skill läuft ohne Browser. Nur für `BROWSER_AUDIT` wird **Python Playwright >=1.48** plus Chromium benötigt; nach Betreiberfreigabe separat installieren (`python3 -m pip install "playwright>=1.48"` und `python3 -m playwright install chromium`). Die Browserprüfungen starten nicht automatisch und benötigen einen vom Nutzer benannten URL- und Pfad-Scope. Details in `references/browser-ux-audit.md`.
