# UPDATE – Precision release (2026-10-20)

## Preserved
Four operating modes, claim/evidence/anti-Dark-Pattern gates, existing tech stack preservation, conversion outcomes and guardrails, accessibility QA, read-only fixture evaluator, package validator and Claude Code install semantics. Original 12 fixtures unchanged byte-for-byte.

## Changed
- Bottleneck-first behavior and explicit non-UI bottleneck handling.
- Obligation to state an alternative explanation and falsifier before interventions.
- Limited changes: one primary + up to two dependent interventions, or NO_CHANGE/RESEARCH_FIRST.
- `strategy_version: 2` adds structured decision/evidence/bottleneck/intervention contract; legacy specs without `strategy_version` still accepted unchanged.
- Stronger experiment integrity checks (SRM, event quality, business outcome not CTA clicks).
- 15 additional valid/invalid deterministic fixtures and four runtime-oriented manual output eval definitions.
- Three source-map entries from official W3C and Microsoft Research, plus Baymard's published UX study.

## Not changed / not established
No real Claude Code execution, browser-based acceptance test or lift measurement has been performed. An optimization hypothesis is not evidence of increased CVR.

## Browser UX adapter UPDATE (2026-10-20)

**Original ZIP:** `sha256:ea3bd6cb5fc4d1e1aebe5be69bade7b2bb947500aa3d7ce059cad7f43e97def5` · 70 files. The previous core-parity report carried an earlier v1 baseline hash; updated to the actual supplied input before this UPDATE.

**Added:** `references/browser-ux-audit.md`; `scripts/browser_ux_audit.py`; `scripts/test_browser_ux_audit.py`; `scripts/validate_browser_adapter.py`.

**Changed:** `SKILL.md` adds optional Workflow 1b; README, security/installation/source/eval docs and release/eval/parity reports; package and quick validators now require browser adapter and check static safeguards.

**Preserved:** four work modes, original 27 JSON eval fixtures, baseline psychological schema, claims, legal guardrails and precision-decision engine. Browser remains optional. No dependency installed by skill itself.

**Testing:** 5 policy unit cases PASS, 1 browser synthetic DOM/screenshot case PASS, 1 real localhost network smoke SKIPPED by environment administrator (no assertion of live website success). There is no empirical conversion uplift measurement.
