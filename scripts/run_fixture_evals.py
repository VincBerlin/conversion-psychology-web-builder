#!/usr/bin/env python3
"""Execute deterministic, side-effect-free policy evaluations against local fixtures."""
import json
import sys
from pathlib import Path
from validate_design_spec import check_spec


def evaluate(root):
    directory = root / "evals" / "fixtures"
    rows = []
    for file in sorted(directory.glob("*.json")):
        d = json.loads(file.read_text(encoding="utf-8"))
        expect = d.pop("_expected", None)
        errors = check_spec(d)
        got = "PASS" if not errors else "BLOCK"
        rows.append({"id":file.stem,"expected":expect,"actual":got,"passed": expect == got,"errors":errors})
    return rows


def main():
    root = Path(__file__).resolve().parent.parent
    rows = evaluate(root)
    if len(rows) < 6:
        print("FAIL: insufficient fixture cases",file=sys.stderr)
        return 1
    for row in rows:
        print(("PASS" if row['passed'] else "FAIL")+": "+row['id']+" → "+row['actual'])
    return 0 if all(r['passed'] for r in rows) else 1

if __name__ == '__main__':
    raise SystemExit(main())
