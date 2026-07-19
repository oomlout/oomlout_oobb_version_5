import os
import tempfile
import unittest

from components.withering_hbbd_logo import working


class WitheringHbbdLogoComponentTests(unittest.TestCase):
    def test_action_builds_rounded_square_badge(self):
        result = working.action(
            size=50,
            depth=3,
            depth_engraving=1.5,
            corner_radius=4,
            pos=[1, 2, 3],
        )

        self.assertEqual(len(result), 1)
        wrapper = result[0]
        self.assertEqual(wrapper["type"], "rotation")
        self.assertEqual(wrapper["typetype"], "positive")
        self.assertEqual(wrapper["pos"], [1, 2, 3])
        badge = wrapper["objects"][0]
        self.assertEqual(badge["shape"], "withering_hbbd_logo")
        self.assertEqual(badge["size"], 50)
        self.assertEqual(badge["corner_radius"], 4)
        self.assertEqual(badge["depth_engraving"], 1.5)

    def test_center_anchor_offsets_by_half_depth(self):
        result = working.action(size=50, depth=4, zz="center", pos=[0, 0, 0])
        self.assertEqual(result[0]["pos"], [0, 0, -2])

    def test_metadata_exposes_exact_component_name(self):
        metadata = working.define()
        self.assertEqual(metadata["name"], "withering_hbbd_logo")
        self.assertIn("withering_hbbd_logo", metadata["shape_aliases"])

    def test_render_copies_path_only_svg_and_uses_relative_import(self):
        from solid2 import scad_render

        with tempfile.TemporaryDirectory() as tmp_dir:
            rendered = working.render(
                {
                    "size": 50,
                    "depth": 3,
                    "depth_engraving": 1.5,
                    "corner_radius": 4,
                    "cache_dir": tmp_dir,
                }
            )
            scad = scad_render(rendered)

            copied_svg = os.path.join(tmp_dir, "withering_hbbd_logo.svg")
            self.assertTrue(os.path.exists(copied_svg))
            with open(copied_svg, "r", encoding="utf-8") as infile:
                svg = infile.read()
            self.assertNotIn("<text", svg)
            self.assertIn('import(file = "withering_hbbd_logo.svg"', scad)
            self.assertIn("hull()", scad)
            self.assertIn("scale(v = [41.0, 41.0, 1])", scad)
            self.assertIn("translate(v = [-0.5, -0.5, 0])", scad)


if __name__ == "__main__":
    unittest.main()
