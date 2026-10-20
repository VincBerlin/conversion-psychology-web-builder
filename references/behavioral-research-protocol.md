# Behavioral Research & Minimal Evaluation Protocol

**Aufgabe:** Finde eine beobachtbare Hürde, nicht nachträglich einen psychologischen Effekt. Ohne Nutzerdaten darf ein Experten-Audit Hypothesen liefern, keinen empirischen Nachweis.

## Minimaler Diagnosepfad (abhängig von vorhandenen Rechten/Tools)

1. Beschreibe den konkreten Nutzer-Task, z. B. „Ein lokaler Kunde möchte in unter zwei Minuten einen Termin anfragen“; keine Suggestivfrage „Findest du diesen tollen CTA?“.
2. Führe einen **5-Sekunden-Verständnistest** durch: nach kurzem Blick Fragen „Was wird angeboten?“, „Für wen?“, „Welcher nächste Schritt?“ als qualitatives Verfahren, **keine wissenschaftliche 5-Sekunden-Umsatzschwelle**.
3. Führe einen **First-Click-/Task-Test** durch: Wo klickt die Person zuerst? Erreicht sie den Schritt? Was hemmt sie? Zeichne Wortlaut/Beobachtung getrennt von Interpretation auf.
4. Prüfe den **gesamten Funnel**, inklusive tatsächlicher Formularübermittlung, Bestätigung und erwarteter Folgeschritte; miss nicht nur Sichtbarkeit/Klick des CTA.
5. Vergleiche Desktop und Mobile, inklusive Tastatur, Zoom, Ladefehler, Validierungsfehler, langsamem Netz und „zurück“ aus dem Formular.
6. Trianguliere, wenn möglich, Aggregatdaten, Nutzerbeobachtung und Content-/Prozessfakten. Kein Session Replay oder Heatmap ohne geklärte Legitimation und Privacy-Maßnahmen.

## Beobachtungsregister

Je Beobachtung: `date/period`, `task`, `segment`, `environment`, `observed_behavior`, `user_quote` (nur rechtmäßig und nach Bedarf anonymisiert), `observer_interpretation`, `alternative_explanation`, `confidence`, `consent_or_source`, `affected_step`.

Markiere Erkenntnisse als `OBSERVED` / `QUALITATIVE` / `EXPERT_HYPOTHESIS` / `UNKNOWN`. Verteile niemals erfundene Teilnehmerzahlen, Heatmap-Punkte, Qualitäts-Scores oder Durchlaufquoten.

## Vier Gegenprüfungen vor Freigabe

- **Reversibilität:** Funktioniert die alte Benutzerroute weiterhin bzw. gibt es einen Rollback?
- **Intent-Korrektheit:** Ist die gewünschte Conversion angemessen für Informationsbedarf und Risiko des Nutzers?
- **Leadqualität:** Führt das Design mehr *passende* Kunden zur Aktion oder nur mehr Neugier-Klicks?
- **Zugänglichkeit:** Funktioniert die Lösung auch ohne Maus, Animation oder perfekten Bildschirm?

## Wenn keine Stichprobe / Analytics vorhanden

Liefere 1–3 **explizit ungetestete** Hypothesen mit Evidenzgrad und einfachem, nicht-invasivem Testplan. Sage nicht „Nutzer werden bevorzugen“, sondern „Hypothese: könnte verständlicher sein, zu prüfen über ...“.
