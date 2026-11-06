"""Build concise part READMEs and source-mesh render sheets. No CAD generation or publishing."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import yaml
import trimesh
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
START, END = '<!-- oobb-presentation:start -->', '<!-- oobb-presentation:end -->'
NOTICE = 'AI-generated images and instructions. Errors possible.'
VARIANTS = [('3dpr.stl', 'Default mounting plate'), ('working_oobb.stl', 'OOBB wire-holder mounting plate')]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != content:
        path.write_text(content, encoding='utf-8', newline='\n')


def dump(path, data):
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def markdown(path, body):
    block = START + '\n' + body.rstrip() + '\n' + END + '\n'
    old = path.read_text(encoding='utf-8') if path.exists() else ''
    if START in old or END in old:
        if old.count(START) != 1 or old.count(END) != 1 or old.index(START) > old.index(END):
            raise ValueError(f'Malformed generated block: {path}')
        new = old[:old.index(START)] + block.rstrip('\n') + old[old.index(END) + len(END):]
    else:
        new = block + ('\n' + old if old else '')
    write(path, new)


def plain(value):
    return str(value or '').replace('_', ' ').strip()


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def title(d):
    maker = {'raspberry_pi': 'Raspberry Pi', 'seeed_studio': 'Seeed Studio',
             'adafruit': 'Adafruit', 'sparkfun': 'SparkFun', 'espressif': 'Espressif'}
    brand = maker.get(d.get('manufacturer'), plain(d.get('manufacturer')).title())
    tokens = [plain(d.get(k)) for k in ('type_2', 'type_3') if d.get(k)]
    model = ' '.join(dict.fromkeys(tokens))
    if d.get('manufacturer') == 'raspberry_pi':
        model = plain(d.get('part_number'))
    for a, b in [('rp2040', 'RP2040'), ('rp2350a', 'RP2350A'), ('esp32', 'ESP32'),
                 ('pico', 'Pico'), ('xiao', 'XIAO'), ('qt py', 'QT Py'), ('feather', 'Feather')]:
        model = re.sub(re.escape(a), b, model, flags=re.I)
    return (brand + ' ' + model).strip() or plain(d.get('name', d['id']))


def font(size):
    for p in [Path('C:/Windows/Fonts/segoeui.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)


def sheet(cache, destination, label, dimensions):
    canvas = Image.new('RGB', (1600, 1000), '#f6f4ef')
    for i, view in enumerate(('angle', 'top')):
        im = Image.open(cache / (view + '.png')).convert('RGBA').resize((720, 720), Image.Resampling.LANCZOS)
        canvas.paste(im, (40 + 800 * i, 105), im)
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 35), label, fill='#243a3b', font=font(38))
    draw.text((48, 850), 'Angled view', fill='#3b4b4b', font=font(26))
    draw.text((848, 850), 'Top view', fill='#3b4b4b', font=font(26))
    dims = ' × '.join(f'{v:g}' for v in dimensions)
    draw.text((48, 904), f'Overall size  {dims} mm', fill='#243a3b', font=font(26))
    draw.text((48, 955), 'AI-generated CAD illustration. Errors possible.', fill='#616966', font=font(21))
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, optimize=True)


def find_blender(value):
    if value:
        return value
    if shutil.which('blender'):
        return shutil.which('blender')
    candidates = sorted(Path('C:/Program Files/Blender Foundation').glob('Blender */blender.exe'), reverse=True)
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError('Blender not found. Set BLENDER_EXE or use --blender.')


def record(folder, root):
    d = yaml.safe_load((folder / 'working.yaml').read_text(encoding='utf-8'))
    if not isinstance(d, dict) or not d.get('id'):
        raise ValueError(f'Missing catalogue ID: {folder}')
    if not d['id'].startswith('electronic_breakout_'):
        raise ValueError('This adapter supports electronic_breakout records only; see presentation/CATALOGUE.md')
    config_path = folder / 'presentation/config.json'
    config = json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
    variants = []
    variant_file = folder / 'mounting_variants.json'
    definitions = json.loads(variant_file.read_text(encoding='utf-8'))['variants'] if variant_file.exists() else [dict(source=s,label=l) for s,l in VARIANTS]
    for definition in definitions:
        source, label = definition['source'], definition['label']
        path = folder / source
        if path.exists():
            mesh = trimesh.load_mesh(path)
            dimensions = [round(float(v), 3) for v in mesh.extents]
            key = hashlib.sha256((sha(path) + sha(HERE / 'render_catalogue.py')).encode()).hexdigest()[:24]
            variants.append(dict(definition, sha256=sha(path), key=key,
                                 dimensions_mm=dimensions, image=f'presentation/images/{path.stem}.png'))
        elif variant_file.exists():
            raise FileNotFoundError(f'Missing declared variant: {path}')
    return dict(folder=folder, data=d, config=config, title=config.get('title', title(d)), variants=variants)


def gallery(folder, variants, family):
    canvas = Image.new('RGB', (1600, 760), '#f6f4ef')
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 32), family + ' mounting plates', fill='#243a3b', font=font(38))
    names = {'full_wrap':'Full wrap', 'short_sides':'Two short sides', 'long_side':'One long side'}
    for i, v in enumerate(variants):
        im = Image.open(folder / v['image']).crop((40,105,760,825)).resize((490,490),Image.Resampling.LANCZOS)
        x=30+i*530
        canvas.paste(im,(x,104))
        draw.text((x+12,610), names[v['layout']], fill='#243a3b', font=font(29))
        draw.text((x+12,657), ' × '.join(f'{n:g}' for n in v['dimensions_mm'])+' mm',fill='#3b4b4b',font=font(24))
    draw.text((42,716),'AI-generated CAD illustration. Errors possible.',fill='#616966',font=font(21))
    path='presentation/images/'+family.lower()+'-layouts.png'
    canvas.save(folder/path,optimize=True)
    return path


def build_part(r, root, cache, no_render):
    folder, d, variants, config = r['folder'], r['data'], r['variants'], r['config']
    for v in variants:
        if not (cache / v['key'] / 'top.png').exists() or not (cache / v['key'] / 'angle.png').exists():
            if no_render and (folder / v['image']).exists():
                old_path = folder / 'presentation/manifest.json'
                old = json.loads(old_path.read_text(encoding='utf-8')) if old_path.exists() else {}
                if any(p.get('key') == v['key'] and p.get('source') == v['source'] for p in old.get('variants', [])):
                    shutil.copyfile(folder / v['image'], folder / (Path(v['source']).stem + '_presentation.png'))
                    continue
            raise FileNotFoundError(f"Render missing for {folder.name}/{v['source']}; run without --readme-only")
        sheet_key = hashlib.sha256((sha(Path(__file__)) + v['label'] + str(v['dimensions_mm'])).encode()).hexdigest()[:16]
        cached_sheet = cache / v['key'] / ('sheet-' + sheet_key + '.png')
        if not cached_sheet.exists():
            sheet(cache / v['key'], cached_sheet, v['label'], v['dimensions_mm'])
        (folder / v['image']).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached_sheet, folder / v['image'])
        # Canonical presentation image plus the required copy beside its STL.
        shutil.copyfile(folder / v['image'], folder / (Path(v['source']).stem + '_presentation.png'))
    galleries = {}
    for family in ('Standard', 'Wire-holder'):
        group = [v for v in variants if v.get('family') == family]
        if len(group) == 3:
            galleries[family] = gallery(folder, group, family)
    label = r['title']
    code = str(d.get('md5_6_alpha') or '—')
    board_dimensions = [d.get('breakout_pcb_width'), d.get('breakout_pcb_height')]
    dims = ' × '.join(str(v) for v in board_dimensions) + ' mm' if all(v is not None for v in board_dimensions) else 'See catalogue record'
    spec = plain(d.get('type_4'))
    body = f'# {label}\n\n{NOTICE}\n\n'
    if variants:
        hero = galleries.get('Standard', variants[0]['image'])
        body += f"![AI-generated CAD renders of {cell(label)} mounting plates]({hero})\n\n"
        body += 'Mounting plates for the listed board. Board not shown.\n\n'
        if galleries and all(v.get('geometry', {}).get('m6_hole_diameter_mm') == 6.5 and
                             v.get('geometry', {}).get('head_clear_diameter_mm') == 13
                             for v in variants):
            body += 'M6: Ø6.5 mm holes, Ø13 mm head/nut clearance, 15 mm pitch.\n\n'
    else:
        body += 'Catalogue reference. No printable mesh is available.\n\n'
    body += '## Parts\n\n'
    if variants:
        body += 'One board and one plate. Choose a plate variant.\n\n'
    body += '| Part | Type | Specification | Qty | MD5 alpha |\n| --- | --- | --- | ---: | --- |\n'
    for v in variants:
        size = ' × '.join(f'{n:g}' for n in v['dimensions_mm'])
        short_label = v['label'] if v.get('family') else ('Default plate' if v['source'] == '3dpr.stl' else 'OOBB wire-holder plate')
        body += f"| [{short_label}]({v['source']}) | Printed | {size} mm | 1 | — |\n"
    body += f'| [{cell(label)}](working.yaml) | Hardware | {cell(dims + ("; " + spec if spec else ""))} | 1 | [{code}](working.yaml) |\n'
    for part in config.get('hardware', []):
        body += f"| [{cell(part['name'])}]({part['url']}) | Hardware | {cell(part['specification'])} | {part['quantity']} | "
        body += f"[{part['md5_6_alpha']}]({part['url']}) |\n" if part.get('md5_6_alpha') else '— |\n'
    if 'Wire-holder' in galleries:
        body += f"\n## Wire-holder plates\n\n![AI-generated CAD renders of wire-holder plate layouts]({galleries['Wire-holder']})\n"
    elif len(variants) > 1 and not galleries:
        body += f"\n## OOBB variant\n\n![AI-generated CAD render of the OOBB wire-holder mounting plate]({variants[1]['image']})\n"
    if config.get('installation'):
        body += '\n## Installation\n\n' + '\n'.join(f'{i}. {step}' for i, step in enumerate(config['installation'], 1)) + '\n'
    elif variants:
        body += '\n## Installation\n\nSelect a plate and download its STL. Board fixing hardware is not specified in this record.\n'
    body += '\n## Files\n\n[Catalogue record](working.yaml) · [Render sources](presentation/manifest.json)'
    for source in config.get('sources', []):
        body += f" · [{source['label']}]({source['url']})"
    body += '\n'
    markdown(folder / 'README.md', body)
    manifest = dict(schema=1, id=d['id'], title=label, md5_6_alpha=d.get('md5_6_alpha'),
                    source='working.yaml', source_sha256=sha(folder / 'working.yaml'),
                    board_dimensions_mm=board_dimensions, variants=variants, galleries=galleries,
                    notice=NOTICE, generator='oomlout_oobb_version_5/presentation/scripts/catalogue.py')
    dump(folder / 'presentation/manifest.json', manifest)
    notes = ('# Source notes\n\n' + NOTICE + '\n\n'
             'The STL meshes are mounting plates. They are rendered without changing their geometry. '
             'Overall sizes are measured from mesh bounds in millimetres. Board sizes and MD5 alpha '
             'codes come from working.yaml. The board record code does not identify a printed plate.\n\n'
             'No electronic board, wire holder or unspecified fastener is added to the scene. '
             'The printed variants are alternatives. Board fastening, electrical wiring, '
             'print settings and physical fit are not inferred from a render.\n\n'
             'Full source metadata remains in working.yaml; the README is the shortened public pass. '
             'Use presentation/config.json for reviewed titles, hardware, installation actions and source links. '
             'Rebuild from this folder with `oobb-present`.\n')
    write(folder / 'presentation/README.md', notes)


def build_index(records, root):
    example = next((r for r in records if r['data'].get('md5_6_alpha') == '1owcj'), records[0])
    relative = example['folder'].relative_to(root).as_posix()
    body = '# Electronic breakout mounting plates\n\n' + NOTICE + '\n\n'
    if example['variants']:
        hero = example['variants'][-1]
        has_standard_gallery = len([v for v in example['variants'] if v.get('family') == 'Standard']) == 3
        hero_image = 'presentation/images/standard-layouts.png' if has_standard_gallery else hero['image']
        body += f"![AI-generated CAD renders: {cell(example['title'])} mounting plates]({relative}/{hero_image})\n\n"
    body += f'{len(records)} catalogue entries. Open a part for plate renders, STL downloads and linked parts.\n\n'
    body += f'[Worked example: {example["title"]}]({relative}) · [Rebuild instructions](presentation/README.md)\n\n'
    groups = {}
    for r in records:
        groups.setdefault(plain(r['data'].get('type_1', 'Other')).capitalize(), []).append(r)
    for group, entries in sorted(groups.items()):
        body += f'## {group}\n\n| Board | PCB size (mm) | Variant | MD5 alpha |\n| --- | --- | --- | --- |\n'
        for r in entries:
            d = r['data']
            path = r['folder'].relative_to(root).as_posix()
            dimensions = ' × '.join(str(d.get(k, '—')) for k in ('breakout_pcb_width', 'breakout_pcb_height'))
            variant = plain(d.get('type_4')) or '—'
            body += f"| [{cell(r['title'])}]({path}) | {dimensions} | {cell(variant)} | [{d.get('md5_6_alpha', '—')}]({path}/working.yaml) |\n"
        body += '\n'
    markdown(root / 'README.md', body)
    dump(root / 'presentation/catalogue.json', [dict(id=r['data']['id'], folder=r['folder'].relative_to(root).as_posix(),
          title=r['title'], renders=len(r['variants'])) for r in records])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', nargs='?', type=Path, default=Path.cwd())
    parser.add_argument('--all', action='store_true', help='Process canonical parts/* folders and build the root index')
    parser.add_argument('--include-untracked', action='store_true', help='With --all, include local uncommitted catalogue records')
    parser.add_argument('--readme-only', action='store_true', help='Reuse existing renders; fail if a required image is absent')
    parser.add_argument('--force', action='store_true', help='Rerender each distinct mesh')
    parser.add_argument('--blender', default=os.environ.get('BLENDER_EXE'))
    args = parser.parse_args()
    folder = args.folder.resolve()
    root = Path(git(folder, 'rev-parse', '--show-toplevel'))
    if args.all:
        if folder != root:
            parser.error('--all must be run from the repository root')
        folders = sorted(p.parent for p in (root / 'parts').glob('*/working.yaml')) if args.include_untracked else [root / p for p in git(root, 'ls-files', 'parts/*/working.yaml').splitlines()]
        if not args.include_untracked:
            folders = [p.parent for p in folders]
    else:
        folders = [folder]
    if not folders:
        parser.error('No catalogue records found')
    records = [record(p, root) for p in folders]
    cache = root / 'presentation/.cache'
    cache.mkdir(parents=True, exist_ok=True)
    write(cache / '.gitignore', '*\n')
    jobs = {}
    for r in records:
        for v in r['variants']:
            directory = cache / v['key']
            if args.force or not all((directory / (view + '.png')).exists() for view in ('angle', 'top')):
                directory.mkdir(parents=True, exist_ok=True)
                jobs[v['key']] = dict(key=v['key'], source=str(r['folder'] / v['source']), directory=str(directory))
    if jobs and not args.readme_only:
        dump(cache / 'jobs.json', list(jobs.values()))
        print(f'Rendering {len(jobs)} unique meshes for {len(records)} records.', flush=True)
        with (cache / 'blender.log').open('w', encoding='utf-8') as log:
            result = subprocess.run([find_blender(args.blender), '--background', '--python-exit-code', '1',
                '--python', str(HERE / 'render_catalogue.py'), '--', str(cache / 'jobs.json')], stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'Blender failed ({result.returncode}); see {cache / "blender.log"}')
    for r in records:
        build_part(r, root, cache, args.readme_only)
    if args.all:
        build_index(records, root)
    print(f'Built {len(records)} part pages. No CAD files changed; no Git commit or push performed.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'oobb-present: {exc}', file=sys.stderr)
        sys.exit(1)
