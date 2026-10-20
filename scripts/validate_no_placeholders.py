#!/usr/bin/env python3
"""Block unresolved production placeholders in authored skill instructions."""
import re
import sys
from pathlib import Path

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    pat=re.compile(r'\{\{[A-Z_][A-Z0-9_]*\}\}|\{[A-Z_][A-Z0-9_]*\}')
    problems=[]
    for p in [root/'SKILL.md',*list((root/'references').glob('*.md'))]:
        for m in pat.finditer(p.read_text(encoding='utf-8')):
            problems.append(p.name+':'+m.group(0))
    print('PASS: no unresolved placeholders' if not problems else 'FAIL: '+'; '.join(problems))
    raise SystemExit(bool(problems))
