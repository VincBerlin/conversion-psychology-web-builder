---
name: conversion-psychology-web-builder
description: Plant, baut, analysiert und verbessert conversionorientierte Websites in Claude Code mit evidenzinformierter Persuasionspsychologie, nachvollziehbarer Nutzerführung, vertrauenswürdigen Belegen, zugänglicher Implementierung und CRO-Messplan. Verwenden bei Landingpages, Firmenwebsites, SaaS-, B2B-, lokalen Dienstleister- und E-Commerce-Seiten sowie bei Conversion-Audits und Redesigns.
---

# Conversion Psychology Web Builder

## Ziel und Grenze
Erstelle oder verbessere Websites so, dass passende Besucher ihre **selbstbestimmte, gut informierte Zielaktion** einfacher erreichen. Dies ist ein Entwicklungs- und Diagnoseskill, kein Beweis für Conversion-Uplift. **Zuerst den Engpass, dann die kleinstmögliche Intervention bestimmen; auch `NO_CHANGE` ist eine zulässige Entscheidung.** Psychologische Prinzipien sind **Hypothesen**, keine universellen Umsatzgesetze. Keine gefälschten Testimonials, Referenzen, Knappheiten, Zahlen, Garantien, Zertifikate oder Preise.

## Wann ausführen
- Anfrage zum Bauen/Redesign/Audit einer Website mit Conversion-, CTA-, Verkaufspsychologie-, Funnel-, Kaufentscheidungs- oder Lead-Optimierungsziel.
- `/conversion-psychology-web-builder` ist die explizite Invocation in Claude Code.
- Nicht für bloßes Logo-/Farben-Editing, generische Bugfixes, SEO-only Tasks, rechtliche Gutachten oder Kampagnen-Texte ohne Website-Kontext.

## Modulnavigation (Progressive Disclosure)
- `references/precision-decision-engine.md`: **immer in AUDIT/PLAN/BUILD/OPTIMIZE laden**; Engpass, Priorität, minimaler Eingriff, Gegenhypothese und Change Contract.
- `references/behavioral-research-protocol.md`: nur bei Diagnose-/Research-Fragen oder schwacher Datenlage laden; Nutzeraufgaben, Beobachtung, First-Click und Bias-Kontrolle.
- `references/browser-ux-audit.md`: **nur bei gewünschter Browserprüfung** laden; optionaler begrenzter Playwright-Adapter, URL-Erlaubnis, JSON-Belege, Statusabgrenzung.
- `references/decision-types-and-blueprints.md`: Entscheidungstypen, Awareness und adaptive Seitentemplates.
- `references/psychology-mechanisms.md`: Mechanismenauswahl, Einsatzbedingungen, Gegenargumente.
- `references/copy-and-interaction-system.md`: Copy, Hero, CTAs, Forms, Trust, Pricing und Design.
- `references/design-spec-schema.md`: ausfüllbare, maschinenprüfbare Strategie-Datei und Publikations-/Beleg-Gate.
- `references/measurement-experiments.md`: Outcome, Guardrails, Testdesign und Instrumentierung.
- `references/legal-ethical-guardrails.md`: Dark Patterns, Consent, Recht und vulnerable Zielgruppen.
- `references/security-and-tools.md`: Arbeitsrechte, externe Services, Tracking und Repository-Grenzen.
- `references/source-policy.md` + `references/source-map.md`: Belege und Unsicherheit.
- `references/claude-code-installation.md`: Installation und Invocation.
- Rohrecherche nur bei Bedarf: `references/research/01_Recherche_Persuasionspsychologie_Webdesign.md`. **Nicht als wissenschaftlich oder juristisch validierte Regelquelle behandeln.**

## Workflow 0 – Repo & Auftrag prüfen
1. `pwd`, `git status --short` (falls Git-Repo), README, Projektregeln/CLAUDE.md, vorhandene Komponenten/Design-Tokens, package scripts und bestehende Funnels **lesen**, nicht eigenmächtig ersetzen.
2. Modus erkennen: `AUDIT_ONLY` (keine Änderungen), `PLAN_ONLY` (nur Strategie), `BUILD` (Code nach Nutzerauftrag), `OPTIMIZE` (gezielte Änderungen). Bei `BUILD`/`OPTIMIZE` vorhandenen Stack und Komponenten erhalten, keine unnötige Neuanlage.
3. Primärkonversion und wirtschaftlichen Zieltyp unterscheiden: Kauf, qualifizierter Lead, bestätigte Buchung, Trial-Aktivierung oder Content-Ziel. Klicks auf CTA nie automatisch als Umsatz deklarieren.
4. Intake knapp erfassen: Branche/Leistung, Land/Rechtsraum, Zielgruppe, Traffic/Intent, Angebotsfakten, Preis, Markenstil, vorhandene Belege, Konversionsziel, Ausgangsdaten, technischen Stack und verfügbare Integrationen.
5. Nur bei *blockierender* Unklarheit fragen (max. drei gezielte Fragen). Sonst explizit `MISSING`/`ASSUMPTION`/`SOURCE_NEEDED` protokollieren. Fehlen echte Bewertungen/Logos, diese Sektion weglassen oder im internen Plan als `PROOF_NEEDED` kennzeichnen; **keine Fake-Cards im Live-UI**.

## Workflow 1 – Conversion-Diagnose vor Design
1. Entscheidungstyp anhand Risiko, Preis, Involvement und Kaufzyklus bestimmen: `impulsiv`, `abwaegend`, `hochriskant`, `abo`, `community`; Wechsel zwischen Typen bei mehreren Nutzerpfaden möglich. Lies `references/decision-types-and-blueprints.md`.
2. Awareness und Traffic-Segment festlegen (unaware → most aware), auch für Landingpage-Ad-Message-Match.
3. Formuliere das Nutzerproblem, den angestrebten Fortschritt (JTBD), 3–7 wichtige Einwände, Risikofaktoren, echte Differenzierung und konkrete nächste Handlung.
4. Fogg-Diagnose in Worten: Fehlt Motivation, Leichtigkeit (Ability) oder klarer Prompt? **B=MAP nicht mathematisch zur Conversion-Prognose nutzen.**
5. Primäre Outcome-Kennzahl und Schutzmetriken definieren. Ohne Daten `BASELINE_MISSING`; keine generierte Vorher/Nachher-Prozentzahl.
6. Lies verpflichtend `references/precision-decision-engine.md`. Erzeuge eine **Engpassdiagnose**: Funnel-Stufe, konkrete Beobachtung + Quelle, alternative Erklärung, Priorität P0–P3 und Entscheidung (`SHIP_SAFE_FIX`, `BUILD_AND_TEST`, `RESEARCH_FIRST`, `NO_CHANGE`, `BLOCK`). Technikfehler und unzuverlässige Metriken haben Vorrang vor Copy-Experimenten.
7. Liefere vor Codeänderung einen kompakten `Conversion Brief`: Outcome/Nenner, Segment, Engpass, Evidenzstatus, wichtigste Einwände, Hypothese **mit Falsifikator**, Änderungsumfang und Messplan. Diagnose ohne belastbare Nutzerdaten **als Expertenhypothese kennzeichnen**.

## Workflow 1b – Optionaler gerenderter Browser-Audit
1. Standard ist `REPO_ONLY`; nur bei konkretem `BROWSER_AUDIT`-Auftrag und autorisierter URL `references/browser-ux-audit.md` laden. Niemals Browser-Verfügbarkeit oder Livedaten voraussetzen.
2. Der ausführbare Adapter `scripts/browser_ux_audit.py` nutzt einen frischen unprivilegierten Browserkontext für Desktop und Mobile, bis zu drei explizit genannte Pfade und speichert Screenshot + `browser-ux-report.json` außerhalb des Repo. Keine eigenmächtige Installation von Playwright oder Browser, kein Website-Crawling.
3. Der Adapter blockiert POST/PUT/PATCH/DELETE, fremde Origins, Redirects, WebSockets und Service Workers, führt keine Klicks und keine Formularübermittlung aus. **Auch GET und Seitenskripte können Seiteneffekte haben**, daher bei sensiblen Systemen nur isoliertes Staging; Browsercode ist keine volle Netzwerksandbox.
4. Fasse Beobachtungen (H1-Sichtbarkeit, CTA-Kandidaten, mobile Überläufe, Formularlabels, JS-Fehler) als `OBSERVED`, Hinweise als `HEURISTIC` zusammen. Nutzerverständnis, echte Fehlerzustände, Form-Submit, Kauf/Buchung und Uplift stets `NOT_TESTED`, wenn kein separater autorisierter, abgesicherter Interaktionstest vorliegt.
5. Für jede priorisierte Browserfeststellung Gegenhypothese und eine kleinste Intervention nennen. Ohne nachweisbare Hürde `NO_CHANGE` akzeptieren.

## Workflow 2 – Psychologische Seitenarchitektur
1. Je nach Entscheidungstyp die richtige Informationsreihenfolge wählen; nicht jeden Besucher in denselben 9-Sektionen-Funnel pressen.
2. Jede wichtige Sektion beantwortet eine konkrete Nutzerfrage: Relevanz → Verständnis → Eignung → Beweis → Angebot/Alternativen → Risikoklärung → Handlung → Bestätigung. Reihenfolge nur begründet anpassen.
3. Eine dominante Handlung je Entscheidungspunkt; legitime sekundäre Pfade für Besucher, die noch recherchieren. CTA darf sich konsistent wiederholen.
4. Wähle standardmäßig **nur eine primäre und höchstens zwei notwendige flankierende Änderungen pro Iteration**. Keine Sektion nur deshalb bauen, weil sie in einem Blueprint vorkommt. Wähle nur wenige begründete Mechanismen aus `references/psychology-mechanisms.md`. Pro Mechanismus festhalten: Nutzerproblem, UI, erforderlicher Beleg, potenzieller Backfire, messbare Hypothese.
5. Baue ein `Proof Inventory`: Kundenreview, Fallstudie, Zertifikat, Kapazität, Lieferzeit, Preis, Garantie – jeweils Quelle, Prüfstatus, Veröffentlichungsrecht, Ablaufdatum falls nötig.
6. Falls Personalisierung erforderlich: transparent, datensparsam, überwiegend kontext- oder explizit auswahlbasiert. Keine sensiblen Vulnerabilitäten ausnutzen.
7. Halte das aktuelle Marken-Design ein. Kein generisches „Conversion Template“ erzwingen. Erstelle **Change Contract** nach `precision-decision-engine.md` für jede ausgewählte Intervention: Nutzerhürde → Beleg → Alternativerklärung → kleinste Codeänderung → Outcome/Nenner + Guardrail → Falsifikator → Rollback.

## Workflow 3 – Copy & UI/UX entwickeln
1. Headline konkret: Was, für wen, überprüfbarer Nutzen. Nie frei erfundene Fristen, Einsparungen oder Gewinngarantien.
2. Subline erläutert Mechanismus. CTA beschreibt reale Aktion und Ziel; Risiko-Reducer unter CTA **nur bei wahrer, belegbarer Bedingung**.
3. Problem und Ergebnisbild in Kundensprache; Features in überprüfbare Benefits übersetzen; bei B2B/High-Ticket ausreichend Vergleichsdetails und Rückfragen ermöglichen.
4. Bilder und Videos müssen Ergebnis, Produkt oder echte Personen belegen; vorhandene genehmigte Assets bevorzugen. Keine erfundenen Logos/Fotos als Referenzen ausgeben.
5. Responsive Mobile-first, semantische HTML-Struktur, Tastaturbedienung, sichtbarer Fokus, klare Labels, verständliche Fehlertexte, `prefers-reduced-motion`, geeignete Kontraste. W3C WCAG 2.2 AA als QA-Referenz, 44×44px gern als großzügiges Designziel, **nicht als gesetzliche Universalpflicht**.
6. **Nützliche Reibung nicht blind entfernen:** Eignungsfragen und verständliche Bedingungen können unpassende Leads, Fehlkäufe und Support reduzieren. Prüfe Auswirkungen auf qualifizierte Conversions. Keine unnötigen Felder, Pflichtkonto, fragwürdige Defaults, versteckte Kosten, aufdringliche Overlay-Schleifen oder Blockierung der Ablehnung.
7. Preise/Garantie/Kündigung transparent; bei regulierten Services und Verbraucherverträgen `LEGAL_REVIEW_REQUIRED`, falls Rechtsprüfung nicht nachgewiesen.

## Workflow 4 – In vorhandenes Projekt integrieren
1. Mit bestehendem Framework, Dateistruktur, Komponenten, Routing, Sprachsystem und Design-Tokens arbeiten. Keine Major-Dependency-Updates ohne Freigabe.
2. Funktionierende Navigation, Backend-Schnittstellen, Formulare, CMS-Daten und bestehende SEO-Metadaten nicht beschädigen. Keine produktiven Credentials/Secrets lesen oder ausgeben, wenn nicht notwendig.
3. Interaktionen durchgängig implementieren: CTA-Targets existieren, Formulare validieren und haben reale/sicher simulierte Zustände, Loader/Errors/Success, Links funktionieren. Stubs klar als `NOT_CONNECTED` melden.
4. **Change Isolation:** Bewahre bestehende funktionale Pfade, Zielseiten und Brand-Tokens. Trenne Defektfixes von Experimenten, damit Ursachen nicht mit vielen gleichzeitigen Änderungen verschleiert werden. Keine neue Dependency nur zur Darstellung einer psychologischen Heuristik.
5. Instrumentierung nur wenn legitime Rechtsgrundlage/Consent und Toolkonfiguration vorhanden; keine Besucher-IDs, E-Mails oder Gesundheitsdaten als Events/Logs. Für Implementierungsdetails `references/measurement-experiments.md` laden.
6. Keine externen Schreibaktionen, Deployment, Käufe oder CRM-Aktionen ohne bestätigten Scope. Keine API-Schlüssel in Code/Artefakten.

## Workflow 5 – Verifikation und Freigabe
1. Prüfe psychologische Logik und Wahrheitsgehalt anhand `references/legal-ethical-guardrails.md`. `BLOCK` bei Dark Pattern, unbelegten Social-Proof- oder Zahlenclaims, falscher Verknappung, manipulativen Consent-Defaults.
2. Prüfe relevante Nutzerwege auf Mobile + Desktop, Tastatur, Formular/Checkout, Fehler- und Leerzustände. Optional Browser-Audit nach Workflow 1b mit **tatsächlich erzeugtem Bericht**, sonst `NOT_TESTED`. Die read-only Beobachtung **testet keine** echten Submits/Checkouts. Führe nur **zum Repository passende** Tests/Builds aus; fehlenden Zugriff offen markieren.
3. Performance: LCP, INP, CLS *messen*, sofern verfügbar. Ziele LCP ≤2,5 s, INP ≤200 ms, CLS ≤0,1 am 75. Perzentil als Web-Vitals-Richtwerte, keine Garantie; Quelle in `source-map.md`.
4. Qualitätsprüfung: Marketingclaim ↔ Proof, CTA ↔ **tatsächlicher erfolgreicher Outcome**, Guardrails und Gegenhypothese. Prüfe bei randomisierten Experimenten zusätzlich Zuteilung/Sample-Ratio-Mismatch, definierte Auswertung und Ausschluss fehlerhafter Events. Geschätzter Conversion-Uplift **niemals ohne Versuchsdaten**. Zahlen ohne Messung ausschließlich als `HYPOTHESIS`, nie als Ergebnisaussage.
5. Für neue Arbeitsaufträge `strategy_version: 2` und mitgelieferte JSON-Strategie nutzen; `python scripts/validate_design_spec.py <strategie.json>` prüft strukturell. **Vor jeder Freigabe zur Veröffentlichung** zusätzlich `python scripts/validate_design_spec.py <strategie.json> --publish --evidence-root <freigegebenes-verzeichnis>` ausführen. `AUDIT_ONLY`/`PLAN_ONLY` dürfen niemals `SHIP_SAFE_FIX` oder `BUILD_AND_TEST` autorisieren. Legacy-v1 ist nur zur Migration, nicht zur Veröffentlichung.
6. Veröffentlichbare Claims, Social Proof, Verknappung und Tracking benötigen Evidenz- und Freigabe-Artefakte im genehmigten Arbeitsumfang. Der Validator prüft Referenzen/Existenz, **nicht** die Authentizität, Rechtswirksamkeit oder inhaltliche Wahrheit. Menschen müssen Inhalt, Berechtigung, Consent und Publikationskontext verifizieren; andernfalls `BLOCKED_EVIDENCE` bzw. `LEGAL_REVIEW_REQUIRED`. Externe CTA-Ziele sind standardmäßig blockiert und benötigen eine separat überprüfte Implementierungsfreigabe.
7. Ergebnis berichten als: **Diagnose → ausgewählter Engpass → Intervention(en) → Warum nicht die Alternativen? → Change Contract → echte Codeänderungen → QA/Messstatus → nächster Test**. Nicht belegte Annahmen offenlassen. Bei `NO_CHANGE` oder `RESEARCH_FIRST` keine kosmetischen Änderungen erzwingen. **Keine behauptete Conversion-Steigerung ohne valide Messung.**

## Präzisionsregeln gegen Scheingenauigkeit
- Kein generischer 100-Punkte-„Conversion Score“, keine universelle Reihenfolge von Sektionen und keine kontextfreie psychologische Farbzuordnung. Priorität P0–P3 ist **ordinales Arbeitsrouting**, keine statistische Effektmessung.
- „Belegt“ bedeutet eine **geprüfte Quelle mit Veröffentlichungsrecht**, nicht nur das JSON-Flag `verified`; Skripte können Wahrheitsgehalt nicht prüfen. `MEASURED`, `OBSERVED` und `APPROVED` sind keine selbstbestätigenden Beweise. Veröffentlichungs-Gate strikt vom reinen Planungs-Gate trennen.
- Nicht mit „mehr CTA“ oder längeren Funnels beginnen. Wenn der Engpass z. B. im nachgelagerten Vertrieb oder im Angebot liegt, melde ihn als **NON_UI_BOTTLENECK** und baue keine irrelevante UI.
- Bereits gute Nutzerwege nicht allein wegen eines Copywriting-Trends verändern. Berichte transparent, wenn Daten eine Entscheidung nicht tragen.

## Sicherheits-Stop-Regeln
- `BLOCKED_SECURITY`: unautorisierter Zugriff, externe Schreibaktion ohne Genehmigung, Secrets.
- `BLOCKED_EVIDENCE`: Marketingclaims, die in Live-UI sollen, aber nicht belegt sind.
- `BLOCKED_MANIPULATION`: Fake Reviews, Fake Timer, unbelegte Knappheit, Opt-in-Zwang, Hidden Costs, Confirmshaming, Ausnutzen vulnerabler Gruppen.
- `LEGAL_REVIEW_REQUIRED`: relevante Jurisdiktion/Pflicht zweifelhaft; neutrale Umsetzung statt Rechtsversprechen, Freigabe vor Launch.
- Stop = betroffene Funktion nicht implementieren bzw. nicht live schalten; unkritische Teile können weitergebaut werden.

## Beispiel-Aufrufe
- `Bitte /conversion-psychology-web-builder verwende: Baue für unseren lokalen Handwerksbetrieb eine mobiloptimierte Termin-Landingpage; nur echte Bewertungen; Ziel sind qualifizierte Anfragen.`
- `Nutze conversion-psychology-web-builder für ein AUDIT_ONLY der SaaS-Preisseite; ändere keinen Code. Erstelle Hypothesen und priorisierte Tests.`
- `Optimiere diese B2B-Website mit demselben Skill. Ziel ist ein qualifiziertes Erstgespräch, nicht der sofortige Kauf.`
