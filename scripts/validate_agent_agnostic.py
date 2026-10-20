#!/usr/bin/env python3
"""Verify compatibility limitations are not misrepresented as tested runtime parity."""
import json
import sys
from pathlib import Path

def check(root):
    x=[]
    try:
        d=json.loads((root/'reports/agent-compatibility-report.json').read_text(encoding='utf-8'))
        s=(root/'references/agent-agnostic-compatibility.md').read_text(encoding='utf-8')
    except Exception as e:return [str(e)]
    if d.get('target_runtime')!='Claude Code':x.append('target runtime mismatch')
    if d.get('tested_runtimes'):x.append('runtime tests not actually performed')
    if not d.get('not_guaranteed'):x.append('no limits')
    if 'agents/openai.yaml' not in d.get('runtime_specific_components',[]):x.append('missing adapter classification')
    if not all(t in s for t in ['Claude Code','tool availability','UI install']):x.append('missing disclaimers')
    return x

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    x=check(root)
    print('PASS: scoped agent compatibility' if not x else 'FAIL: '+'; '.join(x))
    raise SystemExit(bool(x))
