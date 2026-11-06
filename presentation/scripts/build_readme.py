"""Generate a marked README block and CSV from presentation/project.json.

Standard library only. Copies of this script and its template can be vendored in
a downstream project. No network access, CAD changes or shell execution.
"""
import argparse
import csv
import json
from pathlib import Path
from string import Template

START = '<!-- oobb-presentation:start -->'
END = '<!-- oobb-presentation:end -->'


def table(parts, printed, labels):
    rows = [f'| Ref. | Part | Specification | {labels[0]} | {labels[1]} |',
            '| --- | --- | --- | ---: | ---: |']
    for part in parts:
        target = part.get('stl') if printed else part.get('url')
        name = f"[{part['name']}]({target})" if target else part['name']
        rows.append(f"| {part['ref']} | {name} | {part['spec']} | {part['quantity']} | {part['quantity'] * 2} |")
    return '\n'.join(rows)


def combined_table(data):
    rows=['| Ref. | Type | Part | Specification | Qty. | MD5 alpha |',
          '| --- | --- | --- | --- | ---: | --- |']
    for group,kind in [('printed_parts','Print'),('hardware','Hardware')]:
        for p in data[group]:
            target=p.get('stl') or p.get('url')
            name=f"[{p['name']}]({target})" if target else p['name']
            code=p.get('md5_6_alpha')
            code_target=p.get('short_url') or p.get('url')
            code_link=f'[{code}]({code_target})' if code and code_target else (code or '-')
            rows.append(f"| {p['ref']} | {kind} | {name} | {p['spec']} | {p['quantity']} | {code_link} |")
    return '\n'.join(rows)


def build(root, template):
    root = Path(root).resolve()
    data = json.loads((root / 'presentation/project.json').read_text(encoding='utf-8'))
    fields = dict(data['readme'])
    fields['title'] = data['title']
    labels=data.get('quantity_columns',['One assembly','Two assemblies'])
    fields['printed_table'] = table(data['printed_parts'], True, labels)
    fields['hardware_table'] = table(data['hardware'], False, labels)
    fields['parts_table'] = combined_table(data)
    for key in ('assembly_steps', 'installation_steps'):
        fields[key] = '\n\n'.join(f'{i}. {s}' for i, s in enumerate(fields[key], 1))
    content = Template(Path(template).read_text(encoding='utf-8')).substitute(fields).strip()
    block = f'{START}\n{content}\n{END}'
    readme = root / data.get('readme_filename', 'README.md')
    original = readme.read_text(encoding='utf-8') if readme.exists() else ''
    if START in original:
        if original.count(START) != 1 or original.count(END) != 1:
            raise ValueError('README must contain exactly one presentation block')
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        result = before + block + after
    elif original.strip():
        # Preserve unmarked project content. Migration/removal is an explicit edit.
        result = block + '\n\n' + original
    else:
        result = block + '\n'
    readme.write_text(result, encoding='utf-8')
    out = root / 'presentation/parts.csv'
    with out.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['reference','part','specification','quantity_one_assembly','quantity_two_assemblies','stl_or_catalogue','md5_6_alpha','short_url','verification'])
        for p in data['printed_parts'] + data['hardware']:
            writer.writerow([p['ref'],p['name'],p['spec'],p['quantity'],p['quantity']*2,p.get('stl') or p.get('url',''),p.get('md5_6_alpha',''),p.get('short_url',''),p.get('verification','')])
    return readme


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--template', type=Path, default=Path(__file__).resolve().parents[1]/'templates/README.template.md')
    args = parser.parse_args()
    print(build(args.project, args.template))
