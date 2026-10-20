# Source Map (Auditzusammenfassung)

Vollständige strukturierte Referenzen: `source-map.json`.

- `SRC-USER-001` · `user_provided` · Recherche Persuasionspsychologie im Webdesign, Stand 19.10.2026 · Reliability: Ausgangsmaterial, nicht unabhängig geprüft · Confidence 3; nur als Hypothesenbibliothek.
- `SRC-CLAUDE-001` · `primary` · Anthropic, Claude Code Skills · Confidence 5; aktueller Installationsweg und Frontmatter.
- `SRC-FOGG-001` · `primary` · BJ Fogg Behavior Model · Confidence 4; Modellbegriffe, kein Uplift.
- `SRC-STAN-001` · `primary` · Stanford Credibility 2002 · Confidence 4; 46,1% Kommentare, kein Conversion-Prozentsatz.
- `SRC-WCAG-001` · `primary` · WCAG 2.2 · Confidence 5; Accessibility-Anforderungen und Ausnahmen.
- `SRC-WEBV-001` · `primary` · Google Core Web Vitals · Confidence 5; UX-Messziele, kein Umsatzversprechen.
- `SRC-BAYM-001` · `secondary` (institutseigene Datensynthese) · Baymard Cart Abandonment · Confidence 4 für die **genau definierte** Stichprobe, keine branchenweite SEO-/CRO-Prognose.
- `SRC-BFSG-001` · `primary` · Bundesgesetz BFSG · Confidence 5 für den Normtext, rechtliche Einzelfallanwendung `SOURCE_NEEDED`.
- `SRC-DSA-001` · `primary` · DSA Art. 25 · Confidence 5 für Normtext, Anwendung auf konkreten Kunden `SOURCE_NEEDED`.

`SOURCE_NEEDED`: nicht verifizierte Effektstärken/Zahlen, ELM-/Cialdini-Übertragbarkeit auf jedes Segment, aktuelle Jurisdiktionsprüfung, Kundenclaims, echte Analytics-Baselines.
`MISSING_OPTIONAL`: in der Rohrecherche erwähnte Dateien `02_Conversion-Playbook_Mechanismen.md` und `03_Agent-Briefing_und_Page-Blueprints.md`.

- `SRC-BAYM-FORMS-002` · `secondary` · Baymard Checkout Usability/Formulare · Confidence 4 · Nur Kauf-/Checkout-Kontext, **kein** universeller „weniger Formfelder = immer besser“ Beweis.
- `SRC-WAI-FORM-002` · `primary` · W3C Labels/Controls · Confidence 5 · Formulare müssen bedienbar und beschriftet sein; kein quantifizierter Uplift.
- `SRC-MS-SRM-003` · `primary` · Microsoft Research SRM · Confidence 4 · A/B-Test-Ergebnisse nach Stichproben-Zuteilungsfehlern prüfen.

**UPDATE-Entscheidungen:** `precision-decision-engine.md` und `behavioral-research-protocol.md` sind `derived` (konstruierte operative Verfahren), keine experimentell validierten Psychologie-Gesetze. Insbesondere P0–P3 und maximal drei Interventionen sind Engineering-Konventionen, nicht publizierte Effektgrößen.

## UPDATE: Browser
- `SRC-PLAY-NET-004` · `primary` · Playwright Python Network, https://playwright.dev/python/docs/network · Confidence 5 für API-Funktionsweise; wichtige Grenze: normale `route.continue_()`-Weiterleitungen rufen den Request-Handler nicht bei jeder Weiterleitung neu auf.
- `SRC-PLAY-CTX-005` · `primary` · Playwright BrowserContext, https://playwright.dev/python/docs/api/class-browsercontext · Confidence 5; WebSocket-Routing ab Playwright 1.48 dokumentiert.
- `DERIVED-BROWSER-001` · `derived` · Begrenzter Python-Adapter und heuristic findings; kein wissenschaftlicher Nachweis oder garantierte Sicherheitsisolation.
