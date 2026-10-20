# Evaluation Design

1. Trigger Evals (`evals/trigger_queries.json`): echte Website-CRO-Aufforderungen + Near Misses (Logo-only, bugfix-only, rechtliche Einzelberatung, allgemeines Marketing).
2. Output Evals (`evals/output_evals.json`): qualifizierte B2B-Leads, lokal, E-Commerce, keine Belege, Audit-only, SEO-only und rechtlich unklare Branche; Sollverhalten + Failure Modes.
3. Tool/Policy Evals: `scripts/validate_design_spec.py` auf read-only JSON-Fixtures, idempotent und ohne Seiteneffekte. Positive Fixtures und negative Fälle (Fake Timer, Consent, Claims, Missing CTA, ungültige Typen) werden real ausgeführt von `scripts/run_fixture_evals.py`.
4. Packaging und Strukturvalidatoren prüfen nur **statische Artefakte**. Kein fingierter End-to-End-Claude-Lauf: `reports/eval-results.json` zeigt `claude_runtime_e2e=NOT_RUN` solange kein Live-Run erfolgt.
5. Vor produktivem Kundenprojekt E2E-Test in Claude Code mit realem Repo, A11y-Scan und UI-Review durchführen, Conversion-Hypothesen später mit realen Daten prüfen.


## UPDATE: Precision- und Anti-Overload-Tests

Fixtures 013–027 überprüfen den neuen v2-Contract: vorhandener Evidenzstatus, Gegenhypothese, max. drei Interventionen, begründeter NO_CHANGE-/RESEARCH_FIRST-Pfad, Falsifikator, keine reinen CTA-Klickmetriken als stellvertretende Primärconversion und nur bekannte Muster. Fixtures 001–012 müssen unverändert weiterbestehen.

**Grenze:** Diese JSON-Tests belegen nur die maschinelle Policy-Durchsetzung. Mindestens zwei reale Claude-Code-Projektpiloten mit tatsächlicher Site-/Code-/Browser-QA und gemessene oder qualitative Nutzerfeedbacks bleiben erforderlich, bevor Webdesign-Performance belegt werden kann. Keine Live-Statistik wird durch Fixtures ersetzt.

## Optionaler Browser-Adapter: Tests und Grenzen (UPDATE)
- `python scripts/test_browser_ux_audit.py`: 5 rein deterministische Policy- und Befundtests, 1 gerenderter DOM/Viewport-Screenshot-Smoke ohne Netzwerk und 1 lokaler GET/POST-Blockierungstest.
- `python scripts/validate_browser_adapter.py <skill-dir>`: strukturelle Browser-Guardrails, kein echter Netzwerktest.
- In einer Umgebung mit verwalteter Browsernetzwerk-Sperre wird der lokale Netzwerktest `SKIPPED` gemeldet; **keinesfalls** daraus ein erfolgreich ausgeführtes URL-Audit ableiten.
- Zwei Zielgeräte und bis zu drei manuell festgelegte Pfade. Realer Form-Submit/Checkout bewusst `NOT_TESTED`; dafür später nur autorisierte Staging-/Mock-Tests.
- Keine messbare Conversion-Wirkung ohne separat durchgeführte Nutzer-/Funnel-Studie.

## Unabhängiger Audit-Patch (20.10.2026)
- Negativ-Fixtures 028–050 prüfen Modusentscheidung, CTA-Schema, schädliche Ziele, typfalsche Felder, v2 Provenienzstruktur und Legacy-Migration. Alte 001–027 bleiben unverändert.
- `scripts/test_spec_adversarial.py` prüft fehlerhafte JSON-Typen, sichere Ziele und das fail-closed Publikationsgate.
- `scripts/test_browser_policy_mutation.py` erstellt ausschließlich im Arbeitsspeicher eine unsichere `ALLOW`-Mutation und überprüft, dass dieselben Policy-Oracles sie zurückweisen. Das Release-Gate MUSS die echte Policy ausführen, nicht nur nach Texttokens suchen.
- `scripts/validate_browser_adapter.py` führt zwingend Browser-Policy-Tests und den Mutationstest aus; Packaging muss bei Fehlern abbrechen. Ein optionaler lokaler HTTP-Smoketest darf `SKIP` melden; er darf nie als erfolgreicher Netzwerk-Test ausgewiesen werden.
- Artefaktpräsenz/Metadata-Labels belegen keine authentische Consent-Genehmigung, Marketingwahrheit oder Conversion-Wirkung. Echte Claude-Trigger-/Output-Evals und reale Site-E2E müssen separat erfolgen.
