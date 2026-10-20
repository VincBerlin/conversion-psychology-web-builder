#!/usr/bin/env python3
"""Check distribution shape/limits. This cannot check the Claude Code runtime."""
import json
import sys
from pathlib import Path

def check(root):
    p=root/'reports/installability-report.json'
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:return [str(e)]
    x=[]
    if d.get('artifact_name')!='skill.zip':x.append('wrong filename')
    if d.get('claude_code_project_install_ready') is not True:x.append('not install-ready')
    if d.get('frontend_install_suggestion_status') not in {'prepared','blocked','not_controlled_by_skill'}:x.append('invalid frontend status')
    if not d.get('not_controlled_by_skill'):x.append('missing limitations')
    if d.get('blocking_issues'):x.append('blocking issues present')
    if not (root/'SKILL.md').is_file():x.append('missing entrypoint')
    return x

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    p=check(root)
    print('PASS: distributable structure' if not p else 'FAIL: '+'; '.join(p))
    raise SystemExit(bool(p))
