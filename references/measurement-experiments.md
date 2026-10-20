# Messung, CRO-Evaluation und Datenschutz

## Outcome Hierarchie
1. **North-Star im konkreten Businesskontext**: z. B. qualifizierte Leads/aktive Testnutzer je Besucher; bei E-Commerce Deckungsbeitrag pro Besucher, sofern Daten existieren.
2. Mikroziele: CTA-Klick, Formularstart, Formularabschluss; nie als abgeschlossener Verkauf maskieren.
3. Guardrails: Leadqualität, Reklamationen, Retouren, Kündigungen, Supportlast, Consent-Ablehnungsquote (nicht als zu optimierende Zustimmungsrate), Accessibility, Performance.

## Tracking Contract vor Code
Definiere `event_name`, `trigger`, `denominator`, `deduplication_id`, `consent_requirement`, `property_allowlist` und `test_method`. `lead_submitted` nach bestätigter serverseitiger Verarbeitung, `appointment_confirmed` nur nach erfolgreichem Termin; `purchase_completed` nur nach tatsächlicher Zahlung/Bestätigung.
- Niemals E-Mail, Telefon, Gesundheitsdaten, Namen oder andere PII in Analytics-Events, URLs oder Console loggen.
- Nicht ungefragt Analytics-Provider integrieren. Bei nicht geklärter Consent-Rechtslage Tracking als `NOT_CONFIGURED` dokumentieren.
- Vorher-/Nachher-Baseline nur aus realen, zeitlich abgegrenzten Daten; Segment/Traffic-Quelle und Botfilter benennen.

## Diagnostik vor Statistik
- Mess-Qualitäts-Gate: Prüfe definierte Nutzer-/Session-/Event-Nenner, Dubletten, Bot-Traffic, Zeitzonen, Consent-Abdeckung, Funnel-Reihenfolge, Server-Quittungen und Zuordnung zu Traffic-Quellen. Eine Änderung in Traffic-Mix oder Tracking ist keine nachgewiesene UX-Wirkung.
- **Sample-Ratio-Mismatch (SRM)**: Bei Randomisierung prüfen, ob beobachtete Zuordnung unerwartet vom geplanten Split abweicht. Bei SRM zuerst Ursache untersuchen; nicht einfach Gewinner erklären.
- Eine signifikante Mikro-Conversion darf die primäre Qualitätsmetrik (z.B. bestätigter qualifizierter Lead) nicht überstimmen. Mehrfachtests und Segment-Slicing dürfen nicht nachträglich „Gewinner“ produzieren.
- Keine Fixierung auf p<0,05: vorab Entscheidungskriterium definieren, Unsicherheit und praktische Bedeutung berichten. Ohne ausreichende Power = `INCONCLUSIVE`, nicht `NO_EFFECT`.
- Bei kleinen Websites statt scheinpräzisem A/B-Test gezielt Task-/First-Click-Tests, Interviews und Instrumentierungs-Korrekturen durchführen; `references/behavioral-research-protocol.md`.

## Experiment Template
`hypothesis`: Wenn [konkrete Änderung], dann [Metrik], weil [Mechanismus + Nutzerproblem].
`primary_metric`: definierte Conversion. `guardrail_metrics`: Rückgaben, Leadsqualität etc.
`test_design`: randomisiert A/B (wenn technisch + Traffic möglich) oder qualitatives Usability-Testing.
`eligibility`: ausreichender Datenverkehr, Trackingqualität, Consent, keine kritischen Release-Fehler.
`sample_size`: mit Basisrate, Mindestwirkung, Alpha/Power oder nachvollziehbarer Methode ermitteln; nie erfinden.
`duration`: vorher festlegen, Saisonalität berücksichtigen, nicht bei erstem grünem Signal stoppen.
`decision`: Ship, Iterate, No-effect oder Inconclusive.

## Kleine Sites ohne Experiment-Power
Bevorzuge 5-Sekunden-/First-Click-Tests, qualifizierte Interviews, Funnel-Logging (datenschutzkonform), qualitative Heuristikbewertungen. Keine statistische Signifikanz behaupten.

## Technische Mindestchecks
- SEO und Indexierbarkeit; bei Bedarf Structured Data nur für reale sichtbare Inhalte.
- Chrome/field metrics Core Web Vitals auf 75. Perzentil: LCP gut ≤ 2,5s, INP gut ≤ 200ms, CLS gut ≤ 0,1; keine erreichten Werte ohne Messung melden.
- Keyboard-Tab-Order, Fokus, Kontrast, Screenreader-Smoke, 320/375/768/1280 Breakpoints, Formularerrors und echte Zielaktion.
