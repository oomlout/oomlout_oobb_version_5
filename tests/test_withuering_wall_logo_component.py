import unittest
import tempfile
import os

from components.withuering_wall_logo import working


class WithueringWallLogoComponentTests(unittest.TestCase):
    def test_depth_engraving_defaults_to_full_depth(self):
        result = working.action(radius=18, depth=5, pos=[1, 2, 3])

        self.assertEqual(len(result), 1)
        wrapper = result[0]
        self.assertEqual(wrapper["type"], "rotation")
        self.assertEqual(wrapper["typetype"], "positive")
        self.assertEqual(wrapper["pos"], [1, 2, 3])
        self.assertEqual(wrapper["rot"], [0, 0, 0])
        item = wrapper["objects"][0]
        self.assertEqual(item["shape"], "withuering_wall_logo")
        self.assertEqual(item["radius"], 18)
        self.assertEqual(item["depth"], 5)
        self.assertEqual(item["depth_engraving"], 5)
        self.assertEqual(item["logo_size_radius_percent"], 0.65)
        self.assertEqual(item["pos"], [0, 0, 0])

    def test_depth_engraving_can_be_shallow(self):
        result = working.action(radius=18, depth=5, depth_engraving=1.25)

        self.assertEqual(result[0]["objects"][0]["depth_engraving"], 1.25)

    def test_center_anchor_offsets_by_half_depth(self):
        result = working.action(radius=18, depth=5, zz="center", pos=[0, 0, 0])

        self.assertEqual(result[0]["pos"], [0, 0, -2.5])

    def test_rotation_is_carried_by_wrapper(self):
        result = working.action(radius=18, depth=5, rot=[0, 0, 45])

        self.assertEqual(result[0]["rot"], [0, 0, 45])
        self.assertNotIn("rot", result[0]["objects"][0])

    def test_logo_size_radius_percent_can_be_overridden(self):
        result = working.action(radius=18, depth=5, logo_size_radius_percent=0.75)

        self.assertEqual(result[0]["objects"][0]["logo_size_radius_percent"], 0.75)

    def test_metadata_is_documentation_ready(self):
        metadata = working.define()

        self.assertEqual(metadata["name"], "withuering_wall_logo")
        self.assertIn("withuering_wall_logo", metadata["shape_aliases"])
        self.assertGreaterEqual(len(metadata["variables"]), 3)

    def test_render_copies_svg_and_uses_relative_import(self):
        from solid2 import scad_render

        with tempfile.TemporaryDirectory() as tmp_dir:
            rendered = working.render({"radius": 20, "depth": 3, "depth_engraving": 3, "cache_dir": tmp_dir})
            scad = scad_render(rendered)

            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "withuering_wall_logo.svg")))
            self.assertIn('import(file = "withuering_wall_logo.svg"', scad)
            self.assertNotIn("C:/od/OneDrive", scad)
            self.assertIn("scale(v = [13.0, 13.0, 1])", scad)
            self.assertIn("translate(v = [-0.5, 0, 0])", scad)


if __name__ == "__main__":
    unittest.main()
