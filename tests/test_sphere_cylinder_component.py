import unittest

import opsc
from components.sphere_cylinder import working


class SphereCylinderComponentTests(unittest.TestCase):
    def test_action_preserves_cylinder_style_args(self):
        result = working.action(
            type="positive",
            diameter=18,
            depth=12,
            radius_rounded=3,
            center=True,
            pos=[1, 2, 3],
        )

        self.assertEqual(result[0]["shape"], "sphere_cylinder")
        self.assertEqual(result[0]["diameter"], 18)
        self.assertEqual(result[0]["depth"], 12)
        self.assertEqual(result[0]["radius_rounded"], 3)
        self.assertTrue(result[0]["center"])

    def test_renderer_is_registered(self):
        lookup = opsc._build_component_render_lookup()
        self.assertIn("sphere_cylinder", lookup)
        self.assertTrue(callable(lookup["sphere_cylinder"]))

    def test_render_emits_rounded_edge_parts(self):
        scad = opsc.scad_render(
            opsc.get_opsc_item(
                {
                    "type": "positive",
                    "shape": "sphere_cylinder",
                    "r": 8,
                    "h": 20,
                    "radius_rounded": 2,
                    "pos": [0, 0, 0],
                }
            )
        )

        self.assertIn("cylinder(h = 20, r = 6", scad)
        self.assertIn("cylinder(h = 16, r = 8", scad)
        self.assertEqual(scad.count("rotate_extrude(angle = 360)"), 2)


if __name__ == "__main__":
    unittest.main()
