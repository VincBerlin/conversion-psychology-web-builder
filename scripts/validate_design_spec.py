#!/usr/bin/env python3
"""Fail-closed structural CRO strategy validator. Never substitutes for claim/legal review.

v1 legacy documents remain parseable for migration. Publication mode requires v2
and local evidence references; existence proves neither accuracy nor permission.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote

ALLOWED_MODES = {'AUDIT_ONLY', 'PLAN_ONLY', 'BUILD', 'OPTIMIZE'}
ALLOWED_TYPES = {'impulsiv', 'abwaegend', 'hochriskant', 'abo', 'community'}
PRECISION_EVIDENCE = {'OBSERVED', 'QUALITATIVE', 'EXPERT_HYPOTHESIS', 'UNKNOWN'}
PRECISION_DECISIONS = {'SHIP_SAFE_FIX', 'BUILD_AND_TEST', 'RESEARCH_FIRST', 'NO_CHANGE', 'BLOCK'}
PRIORITIES = {'P0','P1','P2','P3'}
V2_PATTERNS = {'clear_cta','plain_language','navigation_clarity','comparison_table','verified_social_proof','transparency','accessible_form','error_recovery','risk_clarification','product_demo','pricing_clarity','opt_in_progress','scarcity','countdown'}
BLOCKED = {'fake_review','fake_timer','fake_scarcity','preselected_paid_extra','preselected_consent','hidden_cost','confirmshaming','forced_continuity'}
VANITY_METRICS = {'clicks','visits','ctr','button_clicks','page_views','impressions','cta_clicks','click_through_rate'}


def populated(value):
    return isinstance(value,str) and bool(value.strip())


def safe_cta_target(target):
    """Default: origin-relative navigation, same-page anchor, valid email/tel links.

    External hosts require separate, reviewed integration approval and are rejected
    by this general-purpose validator. A backend URL must not be auto-whitelisted.
    """
    if not populated(target) or target.strip() != target or re.search(r'[\x00-\x20\x7f\\]',target):
        return False
    if target.startswith('#'):
        return bool(re.fullmatch(r'#[A-Za-z][A-Za-z0-9_.:-]*', target))
    if target.startswith('mailto:'):
        return bool(re.fullmatch(r'mailto:[A-Za-z0-9_.+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}',target))
    if target.startswith('tel:'):
        return bool(re.fullmatch(r'tel:\+?[0-9()\-]{5,25}', target))
    if not target.startswith('/') or target.startswith('//') or '?' in target or '#' in target:
        return False
    decoded = target
    for _ in range(5):
        next_ = unquote(decoded)
        if next_ == decoded: break
        decoded = next_
    if decoded.startswith('//') or '\\' in decoded or any(segment in {'.','..'} for segment in decoded.split('/')):
        return False
    if any(ord(c)<32 for c in decoded):return False
    return bool(re.fullmatch(r'/[A-Za-z0-9_~/%+.,=:@!$&\'()*;\-]*',target))


def check_spec(d):
    issues=[]
    if not isinstance(d,dict): return ['input must be a JSON object']
    for field in ('project','audience','primary_conversion'):
        if not populated(d.get(field)):issues.append(f'missing nonempty {field}')
    if not isinstance(d.get('mode'),str) or d['mode'] not in ALLOWED_MODES:issues.append('invalid mode')
    if not isinstance(d.get('decision_type'),str) or d['decision_type'] not in ALLOWED_TYPES:issues.append('invalid decision_type')
    cta=d.get('primary_cta')
    if not isinstance(cta,dict) or not populated(cta.get('label')) or not populated(cta.get('target')):
        issues.append('primary_cta needs label and target')
    elif not safe_cta_target(cta['target']):issues.append('primary_cta unsafe or external target (requires separate approval)')
    if not isinstance(d.get('baseline_status'),str) or d['baseline_status'] not in {'BASELINE_MISSING','MEASURED'}:
        issues.append('invalid/missing baseline_status')
    if not isinstance(d.get('tracking_status'),str) or d['tracking_status'] not in {'NOT_CONFIGURED','CONSENT_GATED','ESSENTIAL_ONLY','APPROVED'}:
        issues.append('invalid/missing tracking_status')
    metrics=d.get('guardrail_metrics')
    if not isinstance(metrics,list) or not metrics or any(not populated(m) for m in metrics):
        issues.append('nonempty string guardrail_metrics required')
    if not isinstance(d.get('claims'),list):issues.append('claims must be list')
    else:
        for i,claim in enumerate(d['claims']):
            if not isinstance(claim,dict) or not populated(claim.get('text')):
                issues.append(f'claim[{i}] missing text');continue
            if not isinstance(claim.get('verification_status'),str) or claim['verification_status'] not in {'verified','unverified'}:
                issues.append(f'claim[{i}] invalid verification_status')
            if not isinstance(claim.get('publish',True),bool):issues.append(f'claim[{i}].publish must be boolean')
            if claim.get('publish',True) is not False:
                if claim.get('verification_status')!='verified' or not populated(claim.get('source')):
                    issues.append(f'claim[{i}] public claim without verified source')
                if d.get('strategy_version')==2 and (not populated(claim.get('evidence_ref')) or not populated(claim.get('approval_ref'))):
                    issues.append(f'claim[{i}] v2 published claim requires evidence_ref and approval_ref')
    if not isinstance(d.get('patterns'),list):issues.append('patterns must be list')
    else:
        for i,pattern in enumerate(d['patterns']):
            if not isinstance(pattern,dict):issues.append(f'pattern[{i}] must be object');continue
            t=pattern.get('type')
            if not populated(t):issues.append(f'pattern[{i}] type missing');continue
            if t in BLOCKED:issues.append(f'pattern[{i}] blocked manipulation: {t}')
            if t not in V2_PATTERNS:issues.append(f'pattern[{i}] unknown or unsafe pattern: {t}')
            if t in {'scarcity','countdown'}:
                if not populated(pattern.get('proof_source')):issues.append(f'pattern[{i}] scarcity/urgency requires proof_source')
                if t=='countdown':
                    expiry=pattern.get('expiry')
                    if not populated(expiry):issues.append(f'pattern[{i}] countdown requires expiry')
                    else:
                        try:
                            dt=datetime.fromisoformat(expiry.replace('Z','+00:00'))
                            if dt.tzinfo is None:raise ValueError('timezone required')
                        except (ValueError,OverflowError):issues.append(f'pattern[{i}] expiry must be ISO timestamp with timezone')
                if t=='scarcity' and not populated(pattern.get('inventory_source')):
                    issues.append(f'pattern[{i}] scarcity requires inventory_source')
                if d.get('strategy_version')==2 and (not populated(pattern.get('evidence_ref')) or not populated(pattern.get('approval_ref'))):
                    issues.append(f'pattern[{i}] v2 urgency requires evidence_ref and approval_ref')
    version=d.get('strategy_version')
    if version is not None and (type(version) is not int or version!=2):
        issues.append('unknown strategy_version; omit only for read-only legacy v1 or use 2')
    if version is None and any(k in d for k in ('decision','interventions','bottleneck','evidence_level')):
        issues.append('precision fields require strategy_version: 2')
    if version==2:issues.extend(check_precision_contract(d))
    return issues


def check_precision_contract(d):
    issues=[]
    evidence=d.get('evidence_level');decision=d.get('decision');mode=d.get('mode')
    if not isinstance(evidence,str) or evidence not in PRECISION_EVIDENCE:issues.append('v2 evidence_level missing/invalid')
    if not isinstance(decision,str) or decision not in PRECISION_DECISIONS:issues.append('v2 decision missing/invalid')
    if isinstance(mode,str) and isinstance(decision,str) and mode in {'AUDIT_ONLY','PLAN_ONLY'} and decision in {'SHIP_SAFE_FIX','BUILD_AND_TEST'}:
        issues.append('v2 AUDIT_ONLY/PLAN_ONLY cannot authorize build or ship')
    if d.get('baseline_status')=='MEASURED' and not populated(d.get('baseline_evidence_ref')):
        issues.append('v2 MEASURED baseline needs baseline_evidence_ref')
    if d.get('tracking_status')=='APPROVED' and not populated(d.get('tracking_approval_ref')):
        issues.append('v2 APPROVED tracking needs tracking_approval_ref')
    if isinstance(evidence,str) and evidence in {'OBSERVED','QUALITATIVE'} and not populated(d.get('observation_ref')):
        # For safe migration, require a source reference only for publication, see check_publication.
        # This is reported as a WARNING by callers, not a hard structural failure.
        pass
    bottleneck=d.get('bottleneck')
    if not isinstance(bottleneck,dict):issues.append('v2 bottleneck must be object')
    else:
        for field in ('funnel_step','problem','evidence','alternative_explanation'):
            if not populated(bottleneck.get(field)):issues.append(f'v2 bottleneck.{field} missing')
    interventions=d.get('interventions')
    if not isinstance(interventions,list):issues.append('v2 interventions must be list')
    else:
        if len(interventions)>3:issues.append('v2 maximum 3 tightly related interventions per iteration')
        if isinstance(decision,str) and decision in {'NO_CHANGE','BLOCK','RESEARCH_FIRST'} and interventions:
            issues.append('v2 NO_CHANGE/BLOCK/RESEARCH_FIRST must have no authorized interventions')
        if isinstance(decision,str) and decision in {'SHIP_SAFE_FIX','BUILD_AND_TEST'} and not interventions:
            issues.append('v2 build/fix decision needs an intervention')
        for i,item in enumerate(interventions):
            if not isinstance(item,dict):issues.append(f'v2 intervention[{i}] must be object');continue
            for field in ('id','user_problem','mechanism','minimal_change','metric','falsifier','rollback'):
                if not populated(item.get(field)):issues.append(f'v2 intervention[{i}].{field} missing')
            if not isinstance(item.get('priority'),str) or item['priority'] not in PRIORITIES:issues.append(f'v2 intervention[{i}] priority invalid')
            metric=item.get('metric')
            if isinstance(metric,str) and metric.strip().lower() in VANITY_METRICS and d.get('primary_conversion') not in {'informational_click','content_engagement'}:
                issues.append(f'v2 intervention[{i}] vanity metric instead of declared conversion')
    if evidence=='UNKNOWN' and decision=='BUILD_AND_TEST':issues.append('v2 unknown evidence cannot authorize conversion experiment')
    if evidence=='EXPERT_HYPOTHESIS' and decision=='BUILD_AND_TEST' and not populated(d.get('validation_plan')):
        issues.append('v2 expert hypothesis needs concrete validation_plan')
    return issues


def evidence_file(root, value):
    if not populated(value) or value.startswith(('/', '\\')) or ':' in value or '\\' in value:return False
    p=Path(value)
    if any(x in {'.','..'} for x in p.parts):return False
    target=(root/p).resolve()
    try:target.relative_to(root.resolve())
    except ValueError:return False
    return target.is_file() and not target.is_symlink() and target.stat().st_size>0


def check_publication(d, evidence_root):
    """Release gate for file-existence and approvals, not provenance authenticity."""
    issues=[]
    if d.get('strategy_version')!=2: return ['publication requires strategy_version 2; legacy v1 is migration-only']
    if d.get('mode') in {'AUDIT_ONLY','PLAN_ONLY'}:return ['non-building mode cannot authorize publication']
    if d.get('decision') not in {'SHIP_SAFE_FIX','BUILD_AND_TEST'}:
        return ['publication requires an authorized build/fix decision']
    for i,claim in enumerate(d.get('claims', [])):
        if isinstance(claim,dict) and claim.get('publish',True) is not False:
            for key in ('evidence_ref','approval_ref'):
                if not evidence_file(evidence_root,claim.get(key)):
                    issues.append(f'claim[{i}] {key} missing or not locally verifiable')
    for i,pattern in enumerate(d.get('patterns', [])):
        if isinstance(pattern,dict) and pattern.get('type') in {'scarcity','countdown','verified_social_proof'}:
            for key in ('evidence_ref','approval_ref'):
                if not evidence_file(evidence_root,pattern.get(key)):
                    issues.append(f'pattern[{i}] {key} missing or not locally verifiable')
    for field,status,reference in [('baseline_status','MEASURED','baseline_evidence_ref'),('tracking_status','APPROVED','tracking_approval_ref')]:
        if d.get(field)==status and not evidence_file(evidence_root,d.get(reference)):
            issues.append(f'{reference} missing or not locally verifiable')
    if d.get('evidence_level') in {'OBSERVED','QUALITATIVE'} and not evidence_file(evidence_root,d.get('observation_ref')):
        issues.append('observation_ref missing or not locally verifiable')
    return issues


def main(argv):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec',help='strategy JSON path')
    parser.add_argument('--publish',action='store_true',help='require v2 and existing local evidence references')
    parser.add_argument('--evidence-root',type=Path,help='explicit authorized evidence root (default spec folder)')
    args=parser.parse_args(argv[1:])
    try:data=json.loads(Path(args.spec).read_text(encoding='utf-8'))
    except (OSError,ValueError) as exc:
        print(f'FAIL: invalid input: {exc}',file=sys.stderr);return 2
    problems=check_spec(data)
    if not problems and args.publish:problems+=check_publication(data, args.evidence_root or Path(args.spec).resolve().parent)
    if problems:
        print('BLOCKED: '+' | '.join(problems),file=sys.stderr);return 1
    print('PASS: structural strategy contract'+(' and local artifact presence (truth NOT certified)' if args.publish else ' (no claim/legal truth certification)'))
    return 0

if __name__=='__main__':raise SystemExit(main(sys.argv))
