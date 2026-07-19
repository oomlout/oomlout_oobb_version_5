import unittest

from components.oobb_sphere_cylinder import working


class OobbSphereCylinderComponentTests(unittest.TestCase):
    def test_default_style_uses_sphere_cylinder(self):
        result = working.action(pos=[0, 0, 0], depth=18, radius=7, radius_rounded=2, mode="true")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["shape"], "sphere_cylinder")
        self.assertEqual(result[0]["r"], 7)
        self.assertEqual(result[0]["h"], 18)
        self.assertEqual(result[0]["radius_rounded"], 2)
        self.assertEqual(result[0]["pos"], [0, 0, -9])

    def test_style_can_switch_to_plain_cylinder(self):
        result = working.action(pos=[0, 0, 0], depth=18, radius=7, radius_rounded=2, style="cylinder", mode="true")

        self.assertEqual(result[0]["shape"], "cylinder")
        self.assertEqual(result[0]["r"], 7)
        self.assertEqual(result[0]["h"], 18)

    def test_default_modes_match_oobb_cylinder_pattern(self):
        result = working.action(pos=[0, 0, 0], depth=6, radius=3)

        self.assertEqual([item["inclusion"] for item in result], ["laser", "3dpr", "true"])


if __name__ == "__main__":
    unittest.main()
