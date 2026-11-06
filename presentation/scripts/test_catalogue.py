"""Regression checks for preservation, tracked-only discovery and offline rebuilds."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import trimesh
import yaml
from PIL import Image

import catalogue


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='oobb presentation ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)

    def part(self, name, mesh=False):
        folder = self.root / 'parts' / name
        folder.mkdir(parents=True)
        (folder / 'working.yaml').write_text(yaml.safe_dump(dict(
            id='electronic_breakout_' + name, manufacturer='example', type_2='controller',
            md5_6_alpha='abc12', breakout_pcb_width=21, breakout_pcb_height=51)))
        if mesh:
            trimesh.creation.box((59, 89, 3)).export(folder / '3dpr.stl')
        return folder

    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(catalogue.HERE / 'catalogue.py'), *map(str, args)],
                              cwd=self.root, capture_output=True, text=True)

    def test_preserve_manual_text_and_idempotency(self):
        file = self.root / 'README.md'
        file.write_text('User introduction.\n\n' + catalogue.START + '\nold\n' + catalogue.END + '\n\nUser appendix.\n')
        catalogue.markdown(file, '# New title\n')
        first = file.read_bytes()
        catalogue.markdown(file, '# New title\n')
        self.assertEqual(file.read_bytes(), first)
        self.assertTrue(file.read_text().startswith('User introduction.'))
        self.assertTrue(file.read_text().endswith('User appendix.\n'))
        file.write_text(catalogue.START + '\nincomplete')
        with self.assertRaises(ValueError):
            catalogue.markdown(file, 'replacement')

    def test_tracked_only_and_no_geometry_reference(self):
        tracked = self.part('tracked')
        local = self.part('local')
        subprocess.run(['git', '-C', str(self.root), 'add', 'parts/tracked/working.yaml'], check=True)
        result = self.run_tool('--all', '--readme-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((tracked / 'README.md').exists())
        self.assertFalse((local / 'README.md').exists())
        self.assertIn('No printable mesh', (tracked / 'README.md').read_text())
        self.assertNotIn('![', (tracked / 'README.md').read_text())
        result = self.run_tool('--all', '--include-untracked', '--readme-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((local / 'README.md').exists())

    def test_missing_render_fails_then_cached_build_keeps_source(self):
        folder = self.part('mesh', mesh=True)
        digest = catalogue.sha(folder / '3dpr.stl')
        failed = self.run_tool(folder, '--readme-only')
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('Render missing', failed.stderr)
        record = catalogue.record(folder, self.root)
        cache = self.root / 'presentation/.cache' / record['variants'][0]['key']
        cache.mkdir(parents=True, exist_ok=True)
        for view in ('top', 'angle'):
            Image.new('RGBA', (32, 32), (0, 177, 183, 255)).save(cache / (view + '.png'))
        succeeded = self.run_tool(folder, '--readme-only')
        self.assertEqual(succeeded.returncode, 0, succeeded.stderr)
        self.assertEqual(catalogue.sha(folder / '3dpr.stl'), digest)
        self.assertTrue((folder / '3dpr_presentation.png').exists())
        manifest = json.loads((folder / 'presentation/manifest.json').read_text())
        self.assertEqual(manifest['variants'][0]['dimensions_mm'], [59, 89, 3])
        # An existing PNG must not hide a changed source when the render cache is absent.
        trimesh.creation.box((60, 89, 3)).export(folder / '3dpr.stl')
        stale = self.run_tool(folder, '--readme-only')
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn('Render missing', stale.stderr)


if __name__ == '__main__':
    unittest.main()
