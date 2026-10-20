# Source Policy – epistemische Grenzen

Quelltypen: `primary`, `secondary`, `user_provided`, `derived`, `uncertain`. `user_provided` ist Kontext, nicht automatisch wissenschaftlich oder rechtlich richtig. Detaillierte Einträge in `source-map.json`, lesbare Übersicht in `source-map.md`.

Confidence 1–5: 4–5 erlaubt **eng an der Primärquelle formulierte** Regeln/Empfehlungen; 3 nur Designhypothese/Annahme; 1–2 als `SOURCE_NEEDED`/`MISSING`, nicht operationalisieren.

Priorität:
1. Technische Claude Code Details aus offizieller Anthropic-Dokumentation, Interface-/Accessibility-Standards aus W3C, Messung aus Google-Dokumentation.
2. Psychologische Forschungsgrundlagen aus verifizierten Original-Primärquellen; nie aus einem Nutzerdokument allein einen allgemeingültigen Conversion-Uplift ableiten.
3. Richtlinien/Gesetze aus offiziellen Originaltexten; bei jedem produktiven Rechtsclaim Geltungsbereich und aktuelles Datum individuell verifizieren.
4. Nutzerrecherche als Referenz für mögliche psychologische Muster, **nicht** als exakte Evidenzklassifikation oder Rechtsexpertise.

Verpflichtende Korrektur aus dem Recherche-Audit: Stanford 46,1% bezieht sich auf **2.440 ausgewertete Glaubwürdigkeits-Kommentare**; in 46,1 % davon wurde das Design erwähnt, nicht 46,1% conversion impact. Die Fogg-Formel `B=MAP` ist ein diagnostisches Modell, keine numerische Umsatzfunktion. WCAG 2.2 AA 2.5.8 nennt 24×24 CSS px mit Ausnahmen; 44×44 ist höheres Designziel/AAA-Ausgangspunkt. BFSG hat sachlichen Anwendungsbereich und Ausnahmen. DSA Art 25 adressiert Online-Plattform-Anbieter. Die Recherche erwähnt einen Entwurfstermin 11.11.2026, **ein Datum nach Stand des Dokuments 19.10.2026**; niemals als bereits eingetreten bezeichnen.

Dynamic claims (Gesetze, API, Tools, Preise, UX Benchmarks) → bei Bedarf aktuelle Primärquellen erneut prüfen, sonst `SOURCE_NEEDED`. Fehlende Dateien `02_Conversion-Playbook_Mechanismen.md` und `03_Agent-Briefing_und_Page-Blueprints.md` sind in der Rohrecherche erwähnt, aber nicht bereitgestellt; `MISSING_OPTIONAL`.
