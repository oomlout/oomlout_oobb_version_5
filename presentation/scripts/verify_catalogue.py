"""Read-only checks of generated catalogue source hashes, images and relative links."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from PIL import Image
import yaml


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root):
    entries = json.loads((root / 'presentation/catalogue.json').read_text(encoding='utf-8'))
    pages = [root / 'README.md']
    meshes, image_count, galleries = set(), 0, 0
    for entry in entries:
        folder = root / entry['folder']
        data = yaml.safe_load((folder / 'working.yaml').read_text(encoding='utf-8'))
        manifest = json.loads((folder / 'presentation/manifest.json').read_text(encoding='utf-8'))
        assert data['id'] == manifest['id'] == entry['id'], folder
        assert digest(folder / 'working.yaml') == manifest['source_sha256'], folder
        assert data.get('md5_6_alpha') == manifest['md5_6_alpha'], folder
        assert entry['renders'] == len(manifest['variants']), folder
        for variant in manifest['variants']:
            assert digest(folder / variant['source']) == variant['sha256'], folder
            image = folder / variant['image']
            with Image.open(image) as im:
                assert im.size == (1600, 1000), image
                im.verify()
            copy = folder / (Path(variant['source']).stem + '_presentation.png')
            assert digest(copy) == digest(image), copy
            meshes.add(variant['sha256'])
            image_count += 1
        for name in manifest.get('galleries', {}).values():
            with Image.open(folder / name) as im:
                assert im.size == (1600, 760), name
                im.verify()
            galleries += 1
        pages.append(folder / 'README.md')
    for page in pages:
        content = page.read_text(encoding='utf-8')
        assert content.count('<!-- oobb-presentation:start -->') == 1, page
        assert content.count('<!-- oobb-presentation:end -->') == 1, page
        assert 'AI-generated images and instructions. Errors possible.' in content, page
        for target in re.findall(r'\]\(([^)]+)\)', content):
            parsed = urlsplit(target)
            if not parsed.scheme and parsed.path:
                path = page.parent / unquote(parsed.path)
                assert path.exists(), f'{page}: missing link {target}'
    return dict(records=len(entries), readmes=len(pages), sheets=image_count, galleries=galleries, unique_meshes=len(meshes),
                result='Source hashes, alpha codes, images and relative links match.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(verify(args.root.resolve()), indent=2))
