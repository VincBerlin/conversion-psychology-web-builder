#!/usr/bin/env python3
"""Check UPDATE declaration, preserved behaviors, precision additions and legacy fixtures.

This validates local artifacts, not semantic parity of Claude Code generations.
"""
import json
import re
import sys
from pathlib import Path

REQUIRED = {'read_existing_repo', 'brief_before_build', 'adaptive_decision_blueprint',
            'verified_claims_only', 'dark_pattern_block', 'permission_boundary',
            'conversion_metrics_and_guardrails', 'accessibility_and_qa', 'no_unmeasured_uplift'}
OLD_FIXTURES = [
    '001-valid-b2b', '002-valid-real-claim', '003-block-unsupported-claim',
    '004-block-fake-timer', '005-block-scarcity-without-source',
    '006-block-preselected-consent', '007-block-missing-cta',
    '008-block-unrecognized-decision', '009-valid-private-hypothesis',
    '010-block-countdown-expiry', '011-block-paid-extra', '012-valid-expiring-offer'
]

def check(root):
    errors=[]
    try:
        d=json.loads((root/'reports/core-functionality-preservation.json').read_text(encoding='utf-8'))
        skill=(root/'SKILL.md').read_text(encoding='utf-8')
    except Exception as err:
        return [str(err)]
    if d.get('mode')!='UPDATE':errors.append('report must identify UPDATE')
    if d.get('prior_skill_parity')!='PRESERVED_STATIC_SCOPE':errors.append('incorrect static parity status')
    if not re.fullmatch('[0-9a-f]{64}',d.get('baseline_zip_sha256','')):errors.append('missing valid baseline sha256')
    if not REQUIRED.issubset(set(d.get('core_invariants',[]))):errors.append('missing declared original invariants')
    if d.get('core_behavior_change') is not False:errors.append('core behavior changed without explicit approval')
    if d.get('claude_runtime_parity')!='NOT_TESTED':errors.append('runtime parity overclaimed')
    for phrase in ['AUDIT_ONLY','PLAN_ONLY','BUILD','OPTIMIZE','BLOCKED_MANIPULATION','BASELINE_MISSING','NO_CHANGE','Falsifikator']:
        if phrase not in skill:errors.append('SKILL.md missing '+phrase)
    for rel in ['references/precision-decision-engine.md','references/behavioral-research-protocol.md']:
        if not (root/rel).is_file():errors.append('missing precision module '+rel)
    if len(d.get('minimal_additions',[]))<3:errors.append('additions not inventoried')
    for stem in OLD_FIXTURES:
        if not (root/'evals/fixtures'/(stem+'.json')).is_file():errors.append('lost old fixture '+stem)
    return errors

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    errors=check(root)
    print('PASS: declared static core preservation + legacy fixture presence' if not errors else 'FAIL: '+'; '.join(errors))
    raise SystemExit(bool(errors))
