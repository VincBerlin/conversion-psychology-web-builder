# Precision Decision Engine – eine Hürde, eine begründete Intervention

**Zweck:** Die Psychologie dient der *Diagnose*, nicht der nachträglichen Rechtfertigung einer Designidee. Wähle niemals einen Mechanismus, bevor Zielhandlung, Segment, Engpass und Beobachtung klar sind. Kein fiktiver Conversion-Score oder prognostizierter Uplift.

## 1. Beobachtung vor Interpretation

Schreibe je problematischem Nutzerweg exakt:

- **Segment und Kontext:** Wer kommt wodurch mit welchem Vorwissen auf welche Seite? Trenne z. B. Ads-Landingpage von organischer B2B-Recherche; Segmentzuordnung nur aus legitimen Aggregaten oder freiwilligen Angaben.
- **Outcome + Denominator:** Was zählt als *erfolgreiche* Aktion? Welcher Nenner passt zur Funnel-Stufe? Mehr Button-Klicks ≠ mehr bestätigte Termine.
- **Ort des Abbruchs:** Eintritt → Verständnis → Eignung → Vertrauen → Vergleich → Handlung → Bestätigung. Nur beobachtete Abbrüche als `OBSERVED` kennzeichnen.
- **Evidenz:** `OBSERVED` (Messdaten mit Definition und Zeitfenster), `QUALITATIVE` (konkrete Nutzerbeobachtung), `EXPERT_HYPOTHESIS` (Heuristik ohne Nutzerdaten) oder `UNKNOWN`. Hypothesen nie als Nutzertatsachen ausgeben.
- **Konkurrierende Erklärung:** Traffic-Qualität, falsches Angebot, Saisonalität, Trackingfehler, Preis, technische Defekte oder nicht passende Zielgruppe? Bei Messfehler zuerst Messung reparieren.

**Priorisierte Evidenzleiter:** technisch verifizierter Funnel + Event-Semantik → direkte Nutzerbeobachtung/Interviews → ausgewertetes VOC-Material → Branchenstudie unter Kontextvorbehalt → Expertenheuristik. Die Rangfolge ist eine operative Triage-Regel, keine wissenschaftlich kalibrierte Gewichtung. Ein einzelner Nutzerkommentar kann dennoch einen konkreten Bug nachweisen.

## 2. Falsifizierbare Engpasshypothese

Für eine Änderung schriftlich festlegen: `Wenn wir [kleinste Änderung] für [Segment] an [Funnel-Stelle] ausführen, sollte [primärer Outcome] im Vergleich zur passenden Referenz [Richtung] ändern, weil [konkret beobachtete Hürde + Mechanismus].` Dazu **Falsifikator** nennen: Was würde zeigen, dass diese Erklärung falsch war? Beispiel: Erhöhte Formularstarts ohne mehr bestätigte qualifizierte Anfragen stützen die Hypothese nicht.

## 3. Auswahlmatrix: Bedingung vor Maßnahme

| Dominanter diagnostizierter Engpass | Erstintervention | Nur wenn | Nicht tun |
|---|---|---|---|
| Nutzer versteht Angebot nicht | klare Kategorie, Zielgruppe, Outcome, Prozess | 5-Sekunden-/First-Click-Test oder nachvollziehbare Copy-Lücke | Emotion, Reviews oder neue Sektionen addieren, bevor die Bedeutung klar ist |
| Menschen finden die passende Leistung nicht | Orientierung, Information Scent, konkret benannte Navigation | tatsächlicher Such-/Navigationskonflikt | Navigation pauschal auf eine feste Zahl reduzieren |
| Nutzen unklar | Vorher-Aufgabe → Mechanismus → prüfbares Ergebnis | Nutzen ist aus Angebotsfakten ableitbar | Resultate, Fristen oder Garantien erfinden |
| Vertrauensdefizit / hoher Einsatz | echte Belege, Bedingungen, Grenzen, Kontakt | Veröffentlichungsrechte und Quelle geklärt | generierte Testimonials, fake Siegel und Zahlen |
| Angebotsvergleich schwierig | vergleichbare Kriterien, Transparenz über Gesamtpreis und Einschränkungen | reale Auswahl/Vertragssituation | künstliche Decoys, Empfehlung als Popularität ausgeben |
| Intent hoch, Aktion scheitert | Friktionsabbau, Error Recovery, klarer CTA, Autofill | nachweisbarer Bedienfehler bzw. Formularproblem | neue Persuasionsbanner oder Urgency einsetzen |
| Unpassende Leads / hohe Stornos | Erwartungsmanagement, Eignungskriterien, ggf. *sinnvolle* Qualifizierungsfelder | Qualität ist primäre geschäftliche Schwäche | nur Formularfelder reduzieren oder Klickrate maximieren |
| Fehlende Kaufbereitschaft | Demo, FAQ, Alternative mit kleiner Verpflichtung | Nutzer braucht berechtigte Bedenkzeit | Druck, Countdown, Exit-Popup-Schleifen |
| Messung inkonsistent | Event-/Attributionsdefinition und QA reparieren | Datenqualität unklar | A/B-Test oder Uplift-Schätzung darauf aufbauen |

## 4. Priorität – ordinal, nicht numerologische Gewissheit

1. **P0 / BLOCKER:** Täuschung, nicht autorisierte Veröffentlichung, gebrochene zentrale Aktion, schwere Accessibility-/Datenschutzprobleme. Zuerst beheben; kein Conversion-Experiment davor.
2. **P1 / OBSERVED_BOTTLENECK:** verifizierbarer Engpass in erfolgskritischem Nutzerweg, technisch klein und rückrollbar.
3. **P2 / EVIDENCE_INFORMED:** qualitativ nachvollziehbare Hürde oder hinreichend plausible, risikoarme Hypothese.
4. **P3 / EXPLORATORY:** schwach gestützte Varianten oder kosmetische Präferenzen ohne belegte Nutzungshürde.

Bei mehreren Kandidaten entscheide mit dokumentierten Kriterien: Nutzerfolgen/Business-Outcome → Evidenzqualität → implementierbare Reversibilität → Aufwand → Risiko. **Nicht** mit erfundener Uplift-Prognose priorisieren. Standardmäßig maximal **eine primäre und zwei flankierende** Interventionen pro Iteration; null ist zulässig. Flankierende Änderungen müssen für die primäre Hypothese notwendig sein. Kleine, eng begrenzte Änderungen sind besser als opportunistisches „Website aufhübschen“.

## 5. Entscheidung: Bauen, forschen oder nichts ändern

- `SHIP_SAFE_FIX`: offensichtlicher Defekt/irreführender Inhalt; QA, keine absurde A/B-Testpflicht.
- `BUILD_AND_TEST`: Ziel klar, Evidenz ausreichend, Risiko beherrschbar, Messung möglich.
- `RESEARCH_FIRST`: wichtiger Verdacht, aber Ursachen unklar; qualitative Erhebung/Instrumentierung vor Redesign.
- `NO_CHANGE`: kein belegter Engpass und keine plausible überprüfbare Verbesserung.
- `BLOCK`: keine Quellenrechte, Dark Pattern, sensible Ausnutzung, fehlende Genehmigung.

## 6. Wiederverwendbarer Change Contract

Für jede ausgewählte Änderung **genau eine Zeile** im Bericht:

`ID | Segment | Funnel-Schritt | Nutzerhürde | Beobachtung/Quelle | Alternativerklärung | psychologischer Mechanismus | kleinste Codeänderung/Dateien | Erfolgskriterium/Nenner | Guardrail | Falsifikator | Rollback | Entscheidung`

Sätze wie „der Button wird 30 % besser performen“ sind ohne vorliegende, passende Testdaten verboten. Ein falsches oder verzerrtes Argument wird nicht dadurch wahr, dass der Skill ihn als psychologisch bezeichnet.
