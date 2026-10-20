#!/usr/bin/env python3
"""Validate evaluation metadata and execute deterministic fixture suite."""
import json
import subprocess
import sys
from pathlib import Path
from run_fixture_evals import evaluate

def check(root):
    problems=[]
    try:
        triggers=json.loads((root/'evals/trigger_queries.json').read_text(encoding='utf-8'))
        outputs=json.loads((root/'evals/output_evals.json').read_text(encoding='utf-8'))
    except Exception as e:return [str(e)]
    if len(triggers)<8 or not {True,False}.issubset({v.get('should_trigger') for v in triggers}):
        problems.append('trigger evals must cover positive and negative')
    if len(outputs)<5:problems.append('insufficient output evals')
    for i,x in enumerate(outputs):
        if any(not x.get(field) for field in ('id','prompt','expected_properties','failure_modes')):
            problems.append(f'output eval {i} incomplete')
    for i,x in enumerate(triggers):
        if any(field not in x for field in ('query','should_trigger','reason')):
            problems.append(f'trigger eval {i} incomplete')
    result=subprocess.run([sys.executable,'-m','unittest','-v','test_spec_adversarial'], cwd=root/'scripts', capture_output=True,text=True,timeout=35)
    if result.returncode or 'OK' not in result.stderr or 'skipped=' in result.stderr:
        problems.append('adversarial unit suite fails: '+result.stderr[-700:])
    rows=evaluate(root)
    if len(rows)<6 or any(not row['passed'] for row in rows):
        problems.append('fixture evals fail')
    return problems

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    errors=check(root)
    print('PASS: eval metadata & fixture execution' if not errors else 'FAIL: '+'; '.join(errors))
    raise SystemExit(bool(errors))
