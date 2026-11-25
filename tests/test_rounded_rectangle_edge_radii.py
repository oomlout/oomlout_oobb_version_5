"""Independent edge radii are opt-in; legacy component output stays identical."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("edge_radii_component", ROOT / "components/oobb_rounded_rectangle_rounded/working.py")
component = importlib.util.module_from_spec(spec)
spec.loader.exec_module(component)


class EdgeRadiiTests(unittest.TestCase):
    def test_legacy_requests_keep_exact_component_output(self):
        cases = [({}, 'e718205c643bbb3b028da878af4494a6e8257210c22f347efe5b95ddcf25369b'),
                 (dict(size=[30,20,8],radius=5,radius_rounded=2), 'eb6b7acace6f0558951995a095ec4b0a90259fdf7775e4ad81cc17f5a3cbc42e'),
                 (dict(size=[36,24,10],radius=6,radius_rounded=3,pos=[1,2,3],rot=[10,20,30],type='negative'),
                  'b5b5df77b3ff162deff10df6aab6fc3917cded09380f6f0d0c74e993e4279a42')]
        for request, expected in cases:
            result = component.action(**request)
            self.assertEqual(hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest(), expected)

    def test_independent_radii_preserve_transform_and_polarity(self):
        for top, bottom in ((1.5,0),(0,1.5),(1,2),(0,0)):
            result = component.action(size=[44,44,3],radius=5,radius_top=top,radius_bottom=bottom,
                                      pos=[4,5,6],rot=[10,20,30],type='negative')[0]
            self.assertEqual(result['pos'],[4,5,6])
            self.assertEqual(result['rot'],[10,20,30])
            self.assertEqual(result['typetype'],'negative')
            params = result['objects'][0]['module_kwargs']
            self.assertEqual((params['radius_top'],params['radius_bottom']),(top,bottom))

    def test_omitted_side_uses_existing_rounding_radius(self):
        result=component.action(size=[30,20,6],radius=5,radius_rounded=2,radius_bottom=0)[0]
        self.assertEqual(result['objects'][0]['module_kwargs']['radius_top'],2)

    def test_invalid_edge_profiles_fail(self):
        for request in (dict(radius_top=-1),dict(radius_top=6),dict(radius_top=2,radius_bottom=2),dict(radius_top=float('nan'))):
            with self.assertRaises(ValueError):
                component.action(size=[44,44,3],radius=5,**request)
