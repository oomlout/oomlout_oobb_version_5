import copy
import unittest

import oobb
import opsc
from components.oobb_wire import working as wire


# Captured from the electronic project's original 3x3x4 mm plate builder.
# Housing runs use header-pocket depth; basic/power have 14 mm length.
# Each box is (size, corner position); these are millimetres, not grid units.
ORIGINAL_BOXES = {
    "basic": [([5.62, 13.97, 6], [-1.54, -3.81, -1]), ([7.62, 14.0, 3.8], [-2.54, -12.74, 1.2]),
              ([15.24, 3.08, 3.8], [-7.62, -15.82, 1.2]), ([10.16, 20, 3.8], [-5.08, -35.82, 1.2])],
    "power": [([3.08, 6.35, 6], [-1.54, -3.81, -1]), ([5.08, 14.0, 3.8], [-2.54, -12.74, 1.2]),
              ([12.7, 3.08, 3.8], [-7.62, -15.82, 1.2]), ([7.62, 20, 3.8], [-5.08, -35.82, 1.2])],
    "motor": [([3.08, 6.35, 6], [-1.54, 3.81, -1]), ([5.08, 16.55, 3.8], [-2.54, -12.74, 1.2]),
              ([10.16, 3.08, 3.8], [-5.08, -15.82, 1.2]), ([5.08, 20, 3.8], [-2.54, -35.82, 1.2])],
    "motor_stepper": [([8.16, 6.35, 6], [-4.08, 3.81, -1]), ([10.16, 16.55, 3.8], [-5.08, -12.74, 1.2]),
                      ([15.24, 3.08, 3.8], [-7.62, -15.82, 1.2]), ([10.16, 20, 3.8], [-5.08, -35.82, 1.2])],
    "i2c": [([8.16, 6.35, 6], [-2.81, 3.81, -1]), ([10.16, 16.55, 3.8], [-3.81, -12.74, 1.2]),
            ([17.78, 3.08, 3.8], [-8.89, -15.82, 1.2]), ([12.7, 20, 3.8], [-6.35, -35.82, 1.2])],
}


class OobbWireTests(unittest.TestCase):
    def test_dupont_housing_clearance_does_not_shrink_with_host(self):
        for name in ORIGINAL_BOXES:
            for host in ({}, {"height": 2.5}, {"height": 4}, {"front_y": -21.75}):
                with self.subTest(wire_type=name, host=host):
                    boxes = wire.action(wire_type=name, **host)[0]["objects"]
                    entry, run, pocket = boxes[:3]
                    self.assertGreaterEqual(run["size"][1], 14)
                    # Keep the housing flush with the header pocket and
                    # connected to the through-entry, even on larger hosts.
                    self.assertAlmostEqual(run["pos"][1], pocket["pos"][1] + pocket["size"][1])
                    self.assertGreaterEqual(run["pos"][1] + run["size"][1] + 1e-9, entry["pos"][1])
                    if name in ("basic", "power") and host != {"height": 4}:
                        self.assertEqual(run["size"][1], 14)

    def test_housing_run_matches_header_depth(self):
        for name in ORIGINAL_BOXES:
            for depth, cutout_depth in ((4, 2.8), (8, 3)):
                with self.subTest(wire_type=name, depth=depth):
                    entry, run, pocket, exit_box = wire.action(
                        wire_type=name, depth=depth, cutout_depth=cutout_depth
                    )[0]["objects"][:4]
                    for box in (run, pocket, exit_box):
                        self.assertAlmostEqual(box["pos"][2], depth - cutout_depth)
                        self.assertAlmostEqual(box["size"][2], cutout_depth + 1)
                    self.assertEqual(entry["pos"][2], -1)
                    self.assertEqual(entry["size"][2], depth + 2)

    def test_original_clearances_for_every_connector(self):
        for name, expected in ORIGINAL_BOXES.items():
            with self.subTest(wire_type=name):
                result = wire.action(wire_type=name)[0]
                self.assertEqual(result["typetype"], "negative")
                boxes = [item for item in result["objects"] if item["shape"] == "cube"]
                self.assertEqual(len(boxes), 4)
                for box, (size, pos) in zip(boxes, expected):
                    for actual, original in zip(box["size"] + box["pos"], size + pos):
                        self.assertAlmostEqual(actual, original)

    def test_polarizing_pin_defaults_on_and_only_removes_notch(self):
        for name in ORIGINAL_BOXES:
            with self.subTest(wire_type=name):
                default = wire.action(wire_type=name)[0]["objects"]
                enabled = wire.action(wire_type=name, polarizing_pin=True)[0]["objects"]
                disabled = wire.action(wire_type=name, polarizing_pin=False)[0]["objects"]
                self.assertEqual(default, enabled)
                self.assertEqual(disabled, [item for item in enabled if item["shape"] != "cylinder"])
                if name in ("basic", "power", "i2c"):
                    notch = enabled[-1]
                    self.assertEqual(notch["r"], 1.5)
                    self.assertEqual(notch["h"], 3.8)
                    self.assertAlmostEqual(notch["pos"][0], -10.85 if name == "i2c" else -9.58)
                    self.assertEqual(notch["pos"][1], -22)
                    self.assertAlmostEqual(notch["pos"][2], 1.2)
                else:
                    self.assertEqual(enabled, disabled)

    def test_public_dispatch_and_multiple_positions(self):
        thing = {"components": [], "components_objects": [], "components_string": []}
        oobb.append_full(thing, shape="oobb_wire", type="negative", wire_type="power",
                         pos=[[0, 0, 0], [50, 0, 0]])
        self.assertEqual(len(thing["components"]), 2)
        self.assertEqual(thing["components"][1][0]["pos"], [50, 0, 0])
        # Real SolidPython assembly catches empty negative-only child groups.
        positive = wire.action(type="positive")
        scad = opsc.scad_render(opsc.opsc_get_object(positive, mode="3dpr"))
        self.assertIn("cube", scad)
        self.assertIn("cylinder", scad)

    def test_transform_moves_the_entire_feature_and_preserves_input(self):
        params = dict(wire_type="i2c", pos=[20, 30, 4], rot=[10, 20, 90],
                      inclusion="3dpr", m="#", rot_shift=[[1, 2, 3], [0, 0, 45]])
        saved = copy.deepcopy(params)
        result = wire.action(**params)[0]
        self.assertEqual(result["objects"], wire.action(wire_type="i2c")[0]["objects"])
        for key in ("pos", "rot", "inclusion", "m", "rot_shift"):
            self.assertEqual(result[key], params[key])
        result["pos"][0] = 999
        self.assertEqual(params, saved)

    def test_optional_plate_is_a_grouped_difference(self):
        result = wire.action(plate=True)[0]
        self.assertEqual(result["typetype"], "positive")
        self.assertEqual(result["objects"][0][0]["type"], "positive")
        self.assertTrue(all(item["type"] == "negative" for item in result["objects"][1:]))
        scad = opsc.scad_render(opsc.opsc_get_object([result], mode="3dpr"))
        self.assertIn("difference()", scad)
        self.assertIn("cube", scad)
        self.assertEqual(wire.action(plate=True, type="negative")[0]["typetype"], "negative")

    def test_host_thickness_and_custom_front_edge(self):
        result = wire.action(depth=8, cutout_depth=3, front_y=-30)[0]["objects"]
        self.assertEqual(result[0]["size"][2], 10)
        self.assertEqual(result[2]["pos"][2], 5)
        self.assertAlmostEqual(result[2]["pos"][1], -23.82)
        self.assertEqual(result[-1]["pos"][1], -30)

    def test_invalid_configuration_fails_explicitly(self):
        for params in ({"wire_type": "typo"}, {"height": 1}, {"depth": 2},
                       {"cutout_depth": 0}, {"width": 0}, {"polarizing_pin": "false"}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                wire.action(**params)


if __name__ == "__main__":
    unittest.main()
