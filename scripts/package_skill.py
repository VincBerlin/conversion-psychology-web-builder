#!/usr/bin/env python3
"""Create the exact skill.zip after validators; one clean skill directory, no symlinks."""
import subprocess
import sys
import zipfile
from pathlib import Path
NAMES=['quick_validate.py','validate_source_map.py','validate_evals.py','validate_release_gate.py','validate_installability.py','validate_agent_agnostic.py','validate_core_parity.py','validate_no_placeholders.py','validate_browser_adapter.py']

def main():
    root=Path(__file__).resolve().parent.parent
    dist=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent
    for name in NAMES:
        result=subprocess.run([sys.executable,str(root/'scripts'/name),str(root)],capture_output=True,text=True,timeout=20)
        print(result.stdout.strip() or result.stderr.strip())
        if result.returncode:return result.returncode
    dist.mkdir(parents=True,exist_ok=True)
    archive=dist/'skill.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for file in sorted(root.rglob('*')):
            if not file.is_file() or file.is_symlink() or '__pycache__' in file.parts or file.suffix in {'.pyc','.pyo'}:continue
            z.write(file, file.relative_to(root.parent))
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        if not names or any(not n.startswith(root.name+'/') or '..' in Path(n).parts for n in names):
            raise RuntimeError('invalid ZIP structure')
        if f'{root.name}/SKILL.md' not in names:raise RuntimeError('missing SKILL.md in ZIP')
        bad=z.testzip()
        if bad:raise RuntimeError('corrupt member: '+bad)
    print('PACKAGED:',archive,'members=',len(names),'bytes=',archive.stat().st_size)
    return 0

if __name__=='__main__':raise SystemExit(main())
