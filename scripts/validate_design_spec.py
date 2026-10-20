#!/usr/bin/env python3
"""Read-only, conservative checks for one proposed conversion strategy JSON.
This validates a contract, not the truth of its source documents or legal compliance.
"""
import json
import sys
from pathlib import Path

ALLOWED_MODES = {"AUDIT_ONLY", "PLAN_ONLY", "BUILD", "OPTIMIZE"}
ALLOWED_TYPES = {"impulsiv", "abwaegend", "hochriskant", "abo", "community"}
PRECISION_EVIDENCE = {"OBSERVED", "QUALITATIVE", "EXPERT_HYPOTHESIS", "UNKNOWN"}
PRECISION_DECISIONS = {"SHIP_SAFE_FIX", "BUILD_AND_TEST", "RESEARCH_FIRST", "NO_CHANGE", "BLOCK"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
V2_PATTERNS = {"clear_cta", "plain_language", "navigation_clarity", "comparison_table", "verified_social_proof", "transparency", "accessible_form", "error_recovery", "risk_clarification", "product_demo", "pricing_clarity", "opt_in_progress", "scarcity", "countdown"}
BLOCKED = {"fake_review", "fake_timer", "fake_scarcity", "preselected_paid_extra", "preselected_consent", "hidden_cost", "confirmshaming", "forced_continuity"}


def check_spec(d):
    issues = []
    if not isinstance(d, dict):
        return ["input must be a JSON object"]
    for field in ("project", "audience", "primary_conversion"):
        if not isinstance(d.get(field), str) or not d[field].strip():
            issues.append(f"missing nonempty {field}")
    if d.get("mode") not in ALLOWED_MODES:
        issues.append("invalid mode")
    if d.get("decision_type") not in ALLOWED_TYPES:
        issues.append("invalid decision_type")
    cta = d.get("primary_cta")
    if not isinstance(cta, dict) or any(not isinstance(cta.get(x), str) or not cta[x].strip() for x in ('label', 'target')):
        issues.append("primary_cta needs label and target")
    if d.get("baseline_status") not in {"BASELINE_MISSING", "MEASURED"}:
        issues.append("invalid/missing baseline_status")
    if d.get("tracking_status") not in {"NOT_CONFIGURED", "CONSENT_GATED", "ESSENTIAL_ONLY", "APPROVED"}:
        issues.append("invalid/missing tracking_status")
    if not isinstance(d.get("guardrail_metrics"), list) or not d["guardrail_metrics"]:
        issues.append("nonempty guardrail_metrics required")
    if not isinstance(d.get("claims"), list):
        issues.append("claims must be list")
    else:
        for i, claim in enumerate(d["claims"]):
            if not isinstance(claim, dict) or not str(claim.get("text", "")).strip():
                issues.append(f"claim[{i}] missing text")
                continue
            if claim.get("verification_status") not in {"verified", "unverified"}:
                issues.append(f"claim[{i}] invalid verification_status")
            if claim.get("publish", True) is not False:
                if claim.get("verification_status") != "verified" or not str(claim.get("source", "")).strip():
                    issues.append(f"claim[{i}] public claim without verified source")
    if not isinstance(d.get("patterns"), list):
        issues.append("patterns must be list")
    else:
        for i, pattern in enumerate(d["patterns"]):
            if not isinstance(pattern, dict):
                issues.append(f"pattern[{i}] must be object")
                continue
            t = pattern.get("type", "")
            if t in BLOCKED:
                issues.append(f"pattern[{i}] blocked manipulation: {t}")
            if t in {"scarcity", "countdown"}:
                if not str(pattern.get("proof_source", "")).strip():
                    issues.append(f"pattern[{i}] scarcity/urgency requires proof_source")
                if t == "countdown" and not str(pattern.get("expiry", "")).strip():
                    issues.append(f"pattern[{i}] countdown requires expiry")
                if t == "scarcity" and not str(pattern.get("inventory_source", "")).strip():
                    issues.append(f"pattern[{i}] scarcity requires inventory_source")
            if not isinstance(t, str) or not t.strip():
                issues.append(f"pattern[{i}] type missing")
    if d.get("strategy_version") is not None and d.get("strategy_version") != 2:
        issues.append("unknown strategy_version; omit it for legacy v1 or use 2")
    if d.get("strategy_version") == 2:
        issues.extend(check_precision_contract(d))
    return issues


def check_precision_contract(d):
    """Structural fail-closed validation for precision v2, not a truth/impact proof."""
    issues = []
    evidence = d.get("evidence_level")
    decision = d.get("decision")
    if evidence not in PRECISION_EVIDENCE:
        issues.append("v2 evidence_level missing/invalid")
    if decision not in PRECISION_DECISIONS:
        issues.append("v2 decision missing/invalid")
    bottleneck = d.get("bottleneck")
    if not isinstance(bottleneck, dict):
        issues.append("v2 bottleneck must be object")
    else:
        for k in ("funnel_step", "problem", "evidence", "alternative_explanation"):
            if not isinstance(bottleneck.get(k), str) or not bottleneck[k].strip():
                issues.append(f"v2 bottleneck.{k} missing")
    interventions = d.get("interventions")
    if not isinstance(interventions, list):
        issues.append("v2 interventions must be list")
    else:
        if len(interventions) > 3:
            issues.append("v2 maximum 3 tightly related interventions per iteration")
        if decision in {"NO_CHANGE", "BLOCK", "RESEARCH_FIRST"} and interventions:
            # Research can have proposals in the narrative, but must not authorize build actions.
            issues.append("v2 NO_CHANGE/BLOCK/RESEARCH_FIRST must have no authorized interventions")
        if decision in {"BUILD_AND_TEST", "SHIP_SAFE_FIX"} and not interventions:
            issues.append("v2 build/fix decision needs an intervention")
        for i, item in enumerate(interventions):
            if not isinstance(item, dict):
                issues.append(f"v2 intervention[{i}] must be object")
                continue
            for k in ("id", "user_problem", "mechanism", "minimal_change", "metric", "falsifier", "rollback"):
                if not isinstance(item.get(k), str) or not item[k].strip():
                    issues.append(f"v2 intervention[{i}].{k} missing")
            if item.get("priority") not in PRIORITIES:
                issues.append(f"v2 intervention[{i}] priority invalid")
            if item.get("metric") in {"clicks", "visits", "ctr"} and d.get("primary_conversion","") not in {"informational_click", "content_engagement"}:
                issues.append(f"v2 intervention[{i}] cannot optimize vanity metric instead of declared conversion")
    if isinstance(d.get("patterns"), list):
        for i, item in enumerate(d["patterns"]):
            if isinstance(item, dict) and item.get("type") not in V2_PATTERNS:
                issues.append(f"v2 pattern[{i}] unrecognized or unsafe type")
    if evidence == "UNKNOWN" and decision in {"BUILD_AND_TEST"}:
        issues.append("v2 unknown evidence cannot authorize a conversion experiment")
    if evidence == "EXPERT_HYPOTHESIS" and decision == "BUILD_AND_TEST":
        # Expert hypotheses can be tried if the claim is low-risk; require explicit validation path.
        plan = d.get("validation_plan")
        if not isinstance(plan, str) or not plan.strip():
            issues.append("v2 expert hypothesis needs concrete validation_plan")
    return issues


def main(argv):
    if len(argv) != 2:
        print("usage: validate_design_spec.py <path-to-conversion-spec.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"FAIL: invalid input: {e}", file=sys.stderr)
        return 2
    problems = check_spec(data)
    if problems:
        print("BLOCKED: " + " | ".join(problems), file=sys.stderr)
        return 1
    print("PASS: static conversion spec checks (not a legal/claim truth audit)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
