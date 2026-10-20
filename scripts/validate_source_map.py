#!/usr/bin/env python3
"""Verify source inventory and epistemic status."""
import json
from pathlib import Path
import sys

def check(root):
    try:
        docs=json.loads((root/'references/source-map.json').read_text(encoding='utf-8'))
        policy=(root/'references/source-policy.md').read_text(encoding='utf-8')
        summary=(root/'references/source-map.md').read_text(encoding='utf-8')
    except Exception as e: return [str(e)]
    issues=[]
    required={'id','type','purpose','reliability','limitations','confidence_default','url','status'}
    ids=set()
    for i,row in enumerate(docs):
        missing=required - set(row)
        if missing: issues.append(f'{i}: missing {sorted(missing)}');continue
        if row['id'] in ids:issues.append('duplicate ID '+row['id'])
        ids.add(row['id'])
        if row['type'] not in {'primary','secondary','user_provided','derived','uncertain'}:issues.append('invalid type')
        if not isinstance(row['confidence_default'],int) or not (1<=row['confidence_default']<=5):issues.append('invalid confidence')
        if row['type']=='user_provided' and row['confidence_default']>3:issues.append('unverified user research rated too high')
        if row['url'].startswith('references/') and not (root/row['url']).is_file():issues.append('missing local '+row['url'])
        if row['id'] not in summary:issues.append('unmapped source '+row['id'])
    for marker in ('SOURCE_NEEDED','MISSING','Confidence','primary','secondary','user_provided'):
        if marker not in policy+summary:issues.append('missing term '+marker)
    if len(docs)<7:issues.append('fewer than seven sources')
    return issues

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
    problems=check(root)
    print('PASS: source map & policy' if not problems else 'FAIL: '+'; '.join(problems))
    raise SystemExit(bool(problems))
