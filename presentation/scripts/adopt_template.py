"""Copy the reusable README/manual tools into an existing project.
Does not modify CAD, create a manifest, or replace the project's README.
"""
import argparse,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('project',type=Path)
parser.add_argument('--update-tools',action='store_true',help='Replace previously vendored helper scripts and template')
args=parser.parse_args();root=args.project.resolve()
if not root.is_dir():raise SystemExit('Target must be an existing project directory')
for folder in ('images','raw','scenes','qa','scripts/lib','templates'):(root/'presentation'/folder).mkdir(parents=True,exist_ok=True)
for src,rel in [('scripts/build_readme.py','scripts/lib/build_readme.py'),('scripts/manual_layout.py','scripts/lib/manual_layout.py'),('scripts/validate_presentation.py','scripts/lib/validate_presentation.py'),('templates/README.template.md','templates/README.template.md')]:
    target=root/'presentation'/rel
    if target.exists() and not args.update_tools:
        print('Kept existing',target)
    else:
        shutil.copy2(BASE/src,target);print('Copied',target)
# Python templates often ignore every directory called lib. These are source tools.
ignore = root/'.gitignore'
if ignore.exists():
    text = ignore.read_text(encoding='utf-8')
    if 'lib/' in text.splitlines() and '!presentation/scripts/lib/' not in text.splitlines():
        ignore.write_text(text.rstrip()+'\n\n# Vendored presentation source tools\n!presentation/scripts/lib/\n!presentation/scripts/lib/*.py\n', encoding='utf-8')
        print('Made vendored presentation tools visible to Git')
print('Next: create project.json using the documented schema and a project-specific render/build script.')
