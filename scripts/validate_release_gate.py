#!/usr/bin/env python3
"""Check real report assertions against required release conditions."""
import json
import sys
from pathlib import Path
from run_fixture_evals import evaluate
from validate_browser_adapter import check as browser_check

def check(root):
    try:
        d=json.loads((root/'reports/release-gate-report.json').read_text(encoding='utf-8'))
        e=json.loads((root/'reports/eval-results.json').read_text(encoding='utf-8'))
    except Exception as err:return [str(err)]
    problems=[]
    rg=d.get('release_gate',{})
    if rg.get('status')!='PASS' or rg.get('allowed_to_package') is not True:problems.append('release is not PASS')
    for key in ('craftsmanship_gate','anti_confabulation_gate','security_gate','bias_gate'):
        if d.get(key,{}).get('status')!='PASS':problems.append(f'{key} not PASS')
    if d.get('anti_confabulation_gate',{}).get('blocked_claims'):problems.append('blocked claims exist')
    if d.get('anti_sycophancy',{}).get('score',99)>=3:problems.append('sycophancy failure')
    rows=evaluate(root)
    if not rows or not all(r['passed'] for r in rows):problems.append('actual eval fixtures failed')
    if e.get('fixture_status')!='PASS' or e.get('fixture_count')!=len(rows) or e.get('fixture_passed')!=sum(r['passed'] for r in rows):
        problems.append('eval report is stale or inconsistent with actual fixtures')
    problems.extend('mandatory browser gate: '+x for x in browser_check(root))
    if e.get('claude_runtime_e2e')!='NOT_RUN':problems.append('incorrect runtime eval status')
    if rg.get('scope')!='static_artifact_release_only':problems.append('release scope overclaimed')
    return problems

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    x=check(root)
    print('PASS: scoped release gate' if not x else 'FAIL: '+'; '.join(x))
    raise SystemExit(bool(x))
