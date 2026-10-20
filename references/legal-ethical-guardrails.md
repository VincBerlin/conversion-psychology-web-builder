# Sicherheits- und Ethik-Policy (DE/EU, Stand der Prüfung 2026-10-20)

Keine Rechtsberatung. Geltung hängt von Geschäftsmodell, Nutzerstatus, Jurisdiktion und Ausnahmen ab. Behaupte keine rechtliche Freigabe ohne individuelle Prüfung. Für Produktionslaunch rechtliche Anforderungen projektspezifisch prüfen (u.a. UWG, Verbraucherrecht, DSGVO/TDDDG, ggf. BFSG, DSA und weitere sektorale Regeln).

## Automatisch zu blockierende Muster
- Fake Rezensionen, Kundenlogos, Mitarbeiterbiografien, Awards, Reichweiten-/Umsatzzahlen.
- Countdown ohne überprüfbare tatsächliche Deadline und korrekte persistente Zustandsquelle; Stockzähler ohne Echtzeit-Inventar.
- Preisvergleich mit erfundenen oder verschleierten Preisen, versteckte Gebühren; optionales kostenpflichtiges Extra voreingestellt.
- Cookie-Consent mit heimlicher Zustimmung, schwieriger Ablehnung, künstlicher visueller Benachteiligung, vorausgewähltem Opt-in.
- Irreführende CTAs, Confirmshaming, Forced Continuity, nicht schließbare Overlays, Nagging, erschwerter Ausstieg.
- Gesundheits-, Geldnot-, Trauer-, Sucht- oder Minderjährigen-Vulnerabilität gezielt als Verkaufsdruck ausnutzen.

## Nicht-übergreifende Rechtsannahmen
- DSA Art. 25 betrifft **Anbieter von Online-Plattformen** und ist kein pauschaler Direktgeltungsnachweis für jede Firmenwebsite.
- Das BFSG erfasst bestimmte Produkte/Dienstleistungen; u.a. Ausnahmen, z. B. für bestimmte Kleinstunternehmen mit Dienstleistungen (§ 3 Abs. 3). WCAG-Implementierung als Best Practice unabhängig vom jeweils anwendbaren gesetzlichen Umfang.
- 30-Tage-Referenzpreis (§ 11 PAngV) bei unter die Norm fallender Rabattwerbung: nicht auf sämtliche Preisdarstellungen übertragen.
- DSGVO/§ 25 TDDDG und Einwilligung: prüfen, ob eingesetzte Tools technisch notwendige oder einwilligungsbedürftige Operationen sind; keine unzulässigen Defaults.
- Sonderanforderungen für Bestell- und Kündigungsbuttons nur bei anwendbaren Verbraucherverträgen, Angebotskontext und Gesetzesstand.
- Digital Fairness Act nicht als bereits geltendes Gesetz ausgeben; bei dynamischen Daten aktuelle offizielle Quelle prüfen.

## 7-Fragen-Prüfung vor Live
Wahr? Vollständig? Versteht die Person die Folgen? Echte Ablehnungs-/Exit-Option? Keine verletzliche Gruppe ausgenutzt? Verhältnismäßig? Würde die Aussage dem Kunden bei Offenlegung standhalten?

## Claim Gate
Jedem öffentlich erscheinenden numerischen, vergleichenden, rechtlichen, gesundheitlichen oder reputationsbezogenen Claim einen prüfbaren Beleg zuordnen oder **weglassen**. `SOURCE_NEEDED` im internen Bericht ist kein Freibrief für Veröffentlichung.

## Rechts-/Risikoreview
- Datenschutz/Einwilligung, rechtliche Pflichttexte, Verbrauchervertrag, Widerruf, Preis- und Rabattrecht, Reviews: `LEGAL_REVIEW_REQUIRED` für unbekannte oder regulierte Punkte.
- Werbeaussagen mit sensiblen Outcomes (Gesundheit, Finanzen): fachliches Fachreview vor Livegang.
- Quellen: https://eur-lex.europa.eu/legal-content/DE-EN/TXT/?uri=CELEX:32022R2065 ; https://www.gesetze-im-internet.de/bfsg/__1.html ; https://www.gesetze-im-internet.de/bfsg/__3.html ; https://www.w3.org/TR/WCAG22/
