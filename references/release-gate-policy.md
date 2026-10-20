# Release-Gate

Das ZIP darf nur entstehen, wenn die **lokalen Struktur-/Fixture-/Packaging-Prüfungen** bestanden wurden, `release_gate.status == PASS`, `allowed_to_package == true`, `blocked_claims == []` und Anti-Sycophancy Score < 3 sind.

Bewertung: (i) Craftsmanship und klare Grenzen, (ii) Anti-Confabulation/Quellendisziplin, (iii) Anti-Sycophancy, (iv) Bias/WEIRD und User-Thesis-Laundering, (v) Security, (vi) Installability, (vii) Core-Invarianten. Dokumentiere, was **nicht** getestet wurde: echtes Triggern in Claude Code, reale Kunden-Website, A/B-Tests und tatsächlicher Conversion-Uplift.

`PASS` bedeutet hier ausschließlich **paketierbarer statisch validierter Skill**, keine nachgewiesene wirtschaftliche Wirkung, rechtliche Zertifizierung oder Runtime-Abnahme.
