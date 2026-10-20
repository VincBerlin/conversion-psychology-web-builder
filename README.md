# Conversion Psychology Web Builder – Claude Code Skill

Modus UPDATE, präzisionsorientiert aus dem vorherigen CREATE-Skill weiterentwickelt und auf die Recherche vom 19.10.2026 gestützt. Projektstruktur und Stoppregeln in `SKILL.md`. Eingangsrecherche unverändert unter `references/research/`, mit Auditanmerkungen in `references/source-policy.md`.

## Installation

Entpacke `skill.zip` und lege den vollständigen Ordner `conversion-psychology-web-builder/` nach `.claude/skills/` im jeweiligen Projekt oder `~/.claude/skills/` für alle Claude Code Projekte. Wenn ein Ordner gleichen Namens existiert, vor Überschreiben Inhalte vergleichen und sichern. Claude Code lädt keine ZIP direkt als Projekt-Skill.

Claude Code Prompt: `/conversion-psychology-web-builder Optimiere die bestehende Website auf qualifizierte Leads. Nutze nur verifizierte Claims, lies zuerst README/CLAUDE.md/git status, und beginne mit einem Conversion Brief.`

## Lokale Validation

Mit Python 3 im entpackten Skill-Verzeichnis: `python scripts/run_fixture_evals.py`, `python scripts/quick_validate.py`, `python scripts/validate_evals.py`, `python scripts/validate_source_map.py`. Die 12 evals sind deterministische Policy-Fixtures, kein echter Claude-Code-/Browser-/Conversion-Test.

## Grenzen

Ohne Zielwebsite kann dieser Release keine realen Kundendaten, Baselines, echte Marketingclaims, Cookie-Implementierung, Frontend-Installation oder tatsächliche Conversion-Wirkung testen. Vor Produktion fachliches Review und E2E-Akzeptanz durchführen.


## Precision Upgrade

Der bestehende Funktionsumfang bleibt erhalten. Neu sind `references/precision-decision-engine.md` (Engpassdiagnose, Priorität, Gegenhypothese, minimale Intervention und NO_CHANGE), `references/behavioral-research-protocol.md`, der optionale JSON-Vertrag `strategy_version: 2`, das verbesserte Mess- und Experiment-Gate sowie adversariale Policy-Fixtures. Keine fiktive Steigerungsrate, kein pauschaler CRO-Punktescore, kein Zwang zum Redesign.

**Ablauf:** `/conversion-psychology-web-builder OPTIMIZE: Identifiziere für [Zielgruppe] und [Conversion-Event] anhand vorhandener Daten den größten Engpass. Gib erst Engpass, Alternativerklärung, Evidenzstatus und die kleinste plausible Intervention an. Implementiere höchstens drei eng zusammenhängende Änderungen; messe bestätigte qualifizierte Anfragen statt CTA-Klicks und liefere einen Rollback-Plan.`

**Installationsgrenze:** Das ZIP wird entpackt, nicht direkt als Claude-Code-Skill ausgeführt. Statischer Validator-PASS ist kein bestandener Claude-Code-Laufzeit- oder Conversion-Test.

## Optional: Browsergestützte UX-Prüfung
Der Skill enthält `scripts/browser_ux_audit.py` als **opt-in Read-only-intended** Playwright-Adapter. Er macht maximal sechs Beobachtungen (maximal drei ausdrücklich erlaubte Pfade × Desktop/Mobile), liefert JSON und First-Viewport-Screenshots; kein Crawl, keine Login-, Formular-, Bestell- oder Consent-Aktionen. Netzwerk-Schreibmethoden und Weiterleitungen werden blockiert, GET-Nebenwirkungen bleiben ein Restrisiko. Siehe `references/browser-ux-audit.md`. Ohne Playwright oder Browser bleibt `REPO_ONLY` möglich.
