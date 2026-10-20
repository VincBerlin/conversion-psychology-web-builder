#!/usr/bin/env python3
"""Enforced browser safety gate: structural checks plus executable negative tests."""
from pathlib import Path
import ast
import subprocess
import sys


def check(root:Path) -> list[str]:
    required=['scripts/browser_ux_audit.py','scripts/test_browser_ux_audit.py',
              'scripts/test_browser_policy_mutation.py','references/browser-ux-audit.md']
    errors=['missing '+rel for rel in required if not (root/rel).is_file()]
    if errors:return errors
    code=(root/'scripts/browser_ux_audit.py').read_text(encoding='utf-8')
    instructions=(root/'references/browser-ux-audit.md').read_text(encoding='utf-8')
    main=(root/'SKILL.md').read_text(encoding='utf-8')
    for term in ['--remote-public','MAX_PAGES = 3','route.fetch(max_redirects=0',
                 'context.route_web_socket','service_workers="block"','BLOCK_WRITE_METHOD',
                 'BLOCK_CROSS_ORIGIN','policy_for_request']:
        if term not in code:errors.append('browser adapter missing: '+term)
    for term in ['GET','Seiteneffekte','kein Login','NOT_TESTED','Form-Submit']:
        if term.lower() not in instructions.lower():errors.append('browser instruction missing '+term)
    for term in ['Workflow 1b','browser-ux-audit.md','BROWSER_AUDIT','NOT_TESTED']:
        if term not in main:errors.append('SKILL.md missing '+term)
    try:ast.parse(code)
    except SyntaxError as exc:errors.append('browser syntax: '+str(exc))
    if errors:return errors
    scriptdir=root/'scripts'
    commands=[
        [sys.executable,'-m','unittest','-v','test_browser_policy_mutation'],
        [sys.executable,'-m','unittest','-v','test_browser_ux_audit.BrowserPolicyTests'],
    ]
    for cmd in commands:
        try:
            r=subprocess.run(cmd,cwd=scriptdir,text=True,capture_output=True,timeout=35)
            if r.returncode or 'OK' not in r.stderr or 'skipped=' in r.stderr:
                errors.append('mandatory browser safety unit gate failed: '+r.stderr[-900:])
        except (OSError,subprocess.TimeoutExpired) as e:
            errors.append('mandatory browser safety unit gate cannot run: '+str(e))
    return errors

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    failures=check(root)
    print('PASS: browser security enforced + mutation rejected' if not failures else 'FAIL: '+'; '.join(failures))
    raise SystemExit(bool(failures))
