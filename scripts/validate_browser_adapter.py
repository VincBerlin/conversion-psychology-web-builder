#!/usr/bin/env python3
"""Static gate for the optional observational Playwright module."""
from pathlib import Path
import ast
import sys


def check(root: Path) -> list[str]:
    files = ["scripts/browser_ux_audit.py","scripts/test_browser_ux_audit.py", "references/browser-ux-audit.md"]
    errors = ["missing " + rel for rel in files if not (root / rel).is_file()]
    if errors: return errors
    code=(root/'scripts/browser_ux_audit.py').read_text(encoding='utf-8')
    instructions=(root/'references/browser-ux-audit.md').read_text(encoding='utf-8')
    main=(root/'SKILL.md').read_text(encoding='utf-8')
    for text in ['--remote-public','MAX_PAGES = 3','route.fetch(max_redirects=0','context.route_web_socket','service_workers="block"','BLOCK_WRITE_METHOD','BLOCK_CROSS_ORIGIN','not_tested', 'make_findings','policy_for_request']:
        if text not in code: errors.append('browser adapter missing policy: '+text)
    for text in ['GET', 'Seiteneffekte', 'kein Login', 'NOT_TESTED','Form-Submit']:
        if text.lower() not in instructions.lower(): errors.append('browser instructions missing '+text)
    for text in ['Workflow 1b','browser-ux-audit.md', 'BROWSER_AUDIT','NOT_TESTED']:
        if text not in main: errors.append('SKILL.md missing '+text)
    try: ast.parse(code)
    except SyntaxError as exc: errors.append('invalid browser script syntax '+str(exc))
    return errors

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    errors=check(root)
    print('PASS: browser adapter static guardrails' if not errors else 'FAIL: '+'; '.join(errors))
    raise SystemExit(bool(errors))
