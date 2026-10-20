# Strategie-Datei für die deterministische Prüfung

Eine JSON-Datei dient als Transfervertrag zwischen Strategiebericht, Implementierung und QA. Sie ist **optional**, wenn kein Dateischreibzugriff besteht; der menschlich lesbare Brief bleibt erforderlich.

Minimalbeispiel (rein fiktives **Beispiel ohne Marketingzahlen**):
```json
{
  "project": "Beispiel Dienstleister",
  "mode": "BUILD",
  "decision_type": "hochriskant",
  "audience": "lokale Unternehmen",
  "primary_conversion": "qualified_consultation_request",
  "primary_cta": {"label": "Erstgespräch anfragen", "target": "/kontakt"},
  "baseline_status": "BASELINE_MISSING",
  "claims": [],
  "patterns": [{"type": "clear_cta", "purpose": "Sichtbarkeit der Termin-Anfrage"}],
  "guardrail_metrics": ["lead_quality", "complaint_rate"],
  "tracking_status": "NOT_CONFIGURED"
}
```

Validator (`scripts/validate_design_spec.py`) prüft Pflichtfelder und rote Flaggen; er ist **keine** Rechts-, Inhalts- oder UX-Abnahme. Zulässige `decision_type`: `impulsiv`, `abwaegend`, `hochriskant`, `abo`, `community`. Zulässige `mode`: `AUDIT_ONLY`, `PLAN_ONLY`, `BUILD`, `OPTIMIZE`. Claim-Objekte brauchen `text`, `verification_status` (`verified` / `unverified`) und für Live-Veröffentlichung `source`. Unverifizierte Claims gelten als Blocker, wenn `publish: true` oder das Feld fehlt (Fail Closed). Pattern-Typen `scarcity` und `countdown` verlangen `proof_source`, `expiry` / `inventory_source` bei Anwendbarkeit. Gesperrte Typen: `fake_review`, `fake_timer`, `fake_scarcity`, `preselected_paid_extra`, `preselected_consent`, `hidden_cost`, `confirmshaming`, `forced_continuity`.

Für tatsächlichen Launch ist zusätzlich ein manuelles vollständiges Claim Inventory und rechtliche Freigabe erforderlich.


## Precision Contract v2 (für neue Projekte empfohlen)

Der bisherige v1-Contract bleibt für vorhandene Integrationen und Fixtures lesbar. **Neue Website-Builds** verwenden `strategy_version: 2`; beim Import alter Projekte keinen silent Rewrite ausführen.

Füge zu den bestehenden Feldern hinzu:

```json
{
  "strategy_version": 2,
  "evidence_level": "EXPERT_HYPOTHESIS",
  "bottleneck": {
    "funnel_step": "understanding",
    "problem": "Besucher erkennen das Serviceangebot nicht",
    "evidence": "Heuristische Prüfung der aktuellen Headline; noch kein Nutzertest",
    "alternative_explanation": "Unpassender Werbetraffic"
  },
  "decision": "BUILD_AND_TEST",
  "validation_plan": "Erstverständnis und qualifizierte Anfragen vor/nach der Änderung mit definierten Nennern prüfen",
  "interventions": [
    {
      "id": "INT-01",
      "user_problem": "Das Angebot ist nicht eindeutig",
      "mechanism": "processing_fluency",
      "minimal_change": "Headline präzisiert, kein neues Modul",
      "metric": "qualified_leads_per_eligible_visitor",
      "falsifier": "Besucher verstehen das Angebot besser, aber geeignete Anfragen steigen nicht",
      "rollback": "Hero-Texte aus der Vorversion wiederherstellen",
      "priority": "P2"
    }
  ]
}
```

Obiges v2-Beispiel ist nur eine *unveröffentlichte Implementierungs- und Testhypothese*, kein bereits gemessener Conversion-Erfolg. Bei `RESEARCH_FIRST` werden die `interventions` stattdessen leer gelassen und zunächst Untersuchungen empfohlen. `evidence_level`: `OBSERVED`, `QUALITATIVE`, `EXPERT_HYPOTHESIS`, `UNKNOWN`. `decision`: `SHIP_SAFE_FIX`, `BUILD_AND_TEST`, `RESEARCH_FIRST`, `NO_CHANGE`, `BLOCK`. `interventions`: 0–3, wobei `NO_CHANGE`/`BLOCK` **0** verlangen. Für `BUILD_AND_TEST`/`SHIP_SAFE_FIX` ist mindestens 1 Intervention erforderlich. Eine `BUILD`/`OPTIMIZE`-Anfrage erlaubt nicht, ohne ausreichende Evidenz den Entscheidungsstatus umzuschreiben.

Jede Intervention braucht benannte Nutzerhürde, Mechanismus, minimalen Eingriff, **echte Outcome-Metrik**, Falsifikator, Rollback und priorisiertes Risiko. Kein numerischer „psychologischer Impact Score“. JSON-Prüfung ist nur eine formale Vorprüfung, nicht Evidenz-, Marketingclaim- oder Browser-QA.
