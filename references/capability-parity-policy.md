# Core-Parity Policy – UPDATE 2026-10-20

Basis: das vom Nutzer bereitgestellte `skill.zip` mit 51 Dateien, SHA256 im Report `reports/core-functionality-preservation.json`. Dieses UPDATE erhält alle bisherigen Modi (`AUDIT_ONLY`, `PLAN_ONLY`, `BUILD`, `OPTIMIZE`), Anti-Dark-Pattern-Regeln, Claim-Freigabe, Repository-Respekt, Layout-Blueprints, responsive Accessibility/Performance, Tracking-Guardrails, Validatoren und ZIP-Struktur.

**Absichtlich geändert:** Diagnose zuerst, Gegenhypothese, minimaler Eingriff, Outcomes `NO_CHANGE`/`RESEARCH_FIRST`, formale v2-Strategie, stärkere adversariale Evaluationsfälle. Originalstrategie v1 wird weiterhin geprüft und bestehende Testfixtures bleiben erhalten. Die fortschrittlichere Prüfung gilt nur, wenn `strategy_version: 2` verwendet wird. Keine heimliche Breaking Change an historischen Strategiedateien.

**Grenzen:** XML-/JSON-/Python-Validatoren sind statische Prüfungen. Keine tatsächliche Claude-Code-Installation oder Browser-UI-Testung im Zielrepo und keine bestätigte Conversion-Wirkung. Das Verzeichnis `agents/openai.yaml` ist optionaler OpenAI-Handoff und wird von Claude Code nicht als Laufzeitkonfiguration genutzt.

**Browser-Update:** Es ist nur ein optionales Beobachtungsmodul `BROWSER_AUDIT` hinzugekommen. `REPO_ONLY` und die bisherigen vier Hauptmodi bleiben vorhanden. Keine Browserpflicht, kein MCP-Client- oder Claude-Code-Laufzeitparitätsversprechen. Browser-Sicherheits- und E2E-Limits siehe `browser-ux-audit.md`.
