# Independent audit vs. patched skill — 20.10.2026

## Scope / ground truth
- Audited input: `conversion-psychology-web-builder-audit.zip` SHA256 `23ea930148df2258d7ebfb0d6d9f690e4f6e0e496f470de3192d97f124a860f8`. Its root `software-audit-report/` is **an audit, not a replacement Skill**.
- Correct baseline skill: last Browser Edition `skill.zip`, SHA256 `9b5efc1e24906b6577404ff8db2c87f67f4680b54b56e49b7b48af91bd061252`, 74 files.
- Mode `UPDATE`; original skill contents not overwritten. 27/27 preexisting JSON fixtures byte-identical, still pass.

## Findings disposition
| Audit finding | Outcome | Evidence / remaining limit |
|---|---|---|
| FIND-GATE-001: unsafe network policy shipped | **PATCHED** | `validate_browser_adapter` runs actual policy oracle and test-only malicious `ALLOW` mutation. Independent poisoned-copy packaging returned 1 with no archive. This is a verified *unit gate*, not OS network isolation. |
| FIND-MODE-002: audit/plan authorizes build | **PATCHED** | v2 matrix rejects `AUDIT_ONLY`/`PLAN_ONLY` with `BUILD_AND_TEST` or `SHIP_SAFE_FIX`; fixture 028–029. |
| FIND-CTA-003: javascript/external target | **PATCHED** | strict local CTA URL, anchor, mailto/tel validation; fixtures 030–032, 049; off-origin URLs require separate user-approved implementation. |
| FIND-JSON-006: type errors | **PATCHED** | v2 type guards, adversarial unittest across wrong field types; fixtures 033–038, 041, 046–047. |
| FIND-PROOF-004 / FIND-MEASURE-010: self-reported proof | **PARTIALLY PATCHED** | v2 publication requires local evidence/approval reference files and metadata for measured/tracking states; no tool can attest authenticity or legal consent based on presence of files. Human review still **SOURCE_NEEDED**. |
| FIND-LEGACY-005 | **PATCHED publication boundary** | v1 structurally readable for migration but `--publish` rejects it. 27 historical fixture semantics remain intact. |
| FIND-RUNTIME-007, FIND-BROWSER-008, FIND-EVAL-009 | **OPEN** | Browser policy/offline DOM tests done; live network smoke skipped, Claude Code E2E and behavior eval not performed. |
| FIND-SUPPLY-011, FIND-RESEARCH-012, FIND-HISTORY-013, FIND-BROWSER-014 | **OPEN / DOCUMENTED** | No live cross-runtime/reproducible pinned supply-chain validation, research effect strength varies, no historic Git tree beyond provided ZIP, network is not fully isolated. |

## Safety and truth limits
The package release gate is `static_artifact_release_only`, not enterprise production approval or a legal compliance certification. `--publish` tests local evidence file existence; it **does not prove truth, consent, validity, origin, or publication rights**. Remote browsing executes untrusted page JavaScript; no absolute read-only guarantee. A real authorized Claude Code target-project trial and outcome monitoring are required separately.

## Test results and decision
- **50/50** strategy fixtures; 27 preexisting files unchanged, 23 new adversarial/positive cases.
- **7/7** spec-adversarial unit tests.
- **2/2** mutation-policy unit tests and **5/5** browser policy tests.
- Offline browser DOM/screenshot smoke: **PASS**.
- Local browser network smoke: **SKIPPED** due to administrator-enforced browser network block.
- Forced malicious browser code in a separate copy: `scripts/package_skill.py` **FAIL, no ZIP** (expected).
- Static packaging validators: **9/9 PASS**.
- Final decision: **PASS for static artefact distribution only; real runtime and commercial claims NOT_TESTED**.
