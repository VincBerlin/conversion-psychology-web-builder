#!/usr/bin/env python3
"""Validate this skill's static paths and frontmatter without external dependencies."""
from pathlib import Path
import re
import sys

REQUIRED = ["SKILL.md","agents/openai.yaml", "references/source-policy.md", "references/source-map.md", "references/source-map.json", "references/security-and-tools.md", "references/eval-design.md", "references/release-gate-policy.md", "references/enterprise-skill-output-evaluator.md", "references/installability-and-distribution.md", "references/agent-agnostic-compatibility.md", "references/capability-parity-policy.md", "references/claude-code-installation.md", "references/design-spec-schema.md", "references/research/01_Recherche_Persuasionspsychologie_Webdesign.md", "scripts/validate_design_spec.py", "scripts/run_fixture_evals.py", "scripts/validate_release_gate.py", "scripts/validate_installability.py", "scripts/validate_agent_agnostic.py", "scripts/validate_core_parity.py", "scripts/validate_evals.py", "scripts/validate_source_map.py", "scripts/validate_no_placeholders.py", "evals/trigger_queries.json", "evals/output_evals.json", "reports/release-gate-report.json", "reports/installability-report.json", "reports/core-functionality-preservation.json", "reports/agent-compatibility-report.json", "reports/eval-results.json", "scripts/browser_ux_audit.py", "scripts/test_browser_ux_audit.py", "scripts/validate_browser_adapter.py", "references/browser-ux-audit.md"]

def validate(root):
    errors = [f"missing {f}" for f in REQUIRED if not (root/f).is_file()]
    if not root.is_dir(): return ["skill root missing"]
    md = (root/"SKILL.md").read_text(encoding="utf-8") if (root/"SKILL.md").exists() else ""
    match = re.match(r"\A---\n(.*?)\n---\n",md,re.S)
    if not match: return errors+["invalid YAML frontmatter"]
    fields={}
    for line in match.group(1).splitlines():
        if ':' not in line:
            errors.append("invalid frontmatter line")
            continue
        k,v=line.split(':',1);fields[k.strip()]=v.strip()
    if set(fields) != {'name','description'}: errors.append('frontmatter requires only name and description')
    name=fields.get('name','')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or name != root.name or len(name)>64:
        errors.append('invalid/mismatched skill name')
    if not (0<len(fields.get('description',''))<=1024):errors.append('invalid description length')
    if len(md.splitlines())>500:errors.append('SKILL.md too long')
    if 'BLOCKED_MANIPULATION' not in md or 'BASELINE_MISSING' not in md or 'AUDIT_ONLY' not in md:
        errors.append('missing core operating modes/gates')
    empty=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.stat().st_size==0]
    if empty: errors.append('empty files '+str(empty))
    return errors

if __name__=='__main__':
    root=(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent).resolve()
    errs=validate(root)
    print('PASS: structure + frontmatter' if not errs else 'FAIL: '+'; '.join(errs))
    raise SystemExit(1 if errs else 0)
