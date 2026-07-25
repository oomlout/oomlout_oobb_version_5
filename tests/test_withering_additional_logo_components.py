import os
import tempfile
import unittest

from components.withering_built_logo import working as built
from components.withering_mtli_logo import working as mtli
from components.withering_root_logo import working as root


CASES = (
    (mtli, "withering_mtli_logo"),
    (built, "withering_built_logo"),
    (root, "withering_root_logo"),
)


class WitheringAdditionalLogoComponentTests(unittest.TestCase):
    def test_actions_and_metadata_use_exact_component_names(self):
        for module, name in CASES:
            with self.subTest(name=name):
                result = module.action(
                    size=50,
                    depth=3,
                    depth_engraving=1.25,
                    corner_radius=4,
                    pos=[1, 2, 3],
                )
                wrapper = result[0]
                badge = wrapper["objects"][0]
                self.assertEqual(wrapper["pos"], [1, 2, 3])
                self.assertEqual(badge["shape"], name)
                self.assertEqual(badge["depth_engraving"], 1.25)
                metadata = module.define()
                self.assertEqual(metadata["name"], name)
                self.assertIn(name, metadata["shape_aliases"])

    def test_render_copies_each_path_only_svg_with_a_relative_import(self):
        from solid2 import scad_render

        for module, name in CASES:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp_dir:
                rendered = module.render(
                    {
                        "size": 50,
                        "depth": 3,
                        "depth_engraving": 1.25,
                        "corner_radius": 4,
                        "cache_dir": tmp_dir,
                    }
                )
                scad = scad_render(rendered)
                copied_svg = os.path.join(tmp_dir, f"{name}.svg")
                self.assertTrue(os.path.exists(copied_svg))
                with open(copied_svg, "r", encoding="utf-8") as infile:
                    svg = infile.read()
                self.assertNotIn("<text", svg)
                self.assertNotIn("<rect", svg)
                self.assertIn(f'import(file = "{name}.svg"', scad)
                self.assertIn("hull()", scad)


if __name__ == "__main__":
    unittest.main()
