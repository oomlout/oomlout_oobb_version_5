import copy
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import oobb
import opsc
from components.oobb_cylinder_d_shaft import working


class OobbCylinderDShaftTests(unittest.TestCase):
    def test_cut_depth_is_removed_mm_for_different_radii(self):
        for radius in (3, 5, 10):
            with self.subTest(radius=radius):
                cylinder, cut = working.action(radius=radius, cut_d=2, depth=12, mode="true")[0]["objects"]
                self.assertEqual(cut["pos"][1], radius - 2)
                self.assertEqual(cut["pos"][1] - (-radius), 2 * radius - 2)
                self.assertLess(cut["pos"][2], cylinder["pos"][2])
                self.assertGreater(cut["pos"][2] + cut["size"][2], cylinder["pos"][2] + cylinder["h"])

    def test_zero_cut_leaves_cylinder_and_deep_cuts_are_allowed(self):
        self.assertEqual(len(working.action(radius=5, cut_d=0, mode="true")[0]["objects"]), 1)
        for cut_d in (5, 9.9):
            self.assertAlmostEqual(working.action(radius=5, cut_d=cut_d, mode="true")[0]["objects"][1]["pos"][1], 5 - cut_d)

    def test_invalid_dimensions_rejected(self):
        for overrides in (
            {"cut_d": -1}, {"cut_d": 10}, {"cut_d": 11}, {"cut_d": float("nan")},
            {"cut_d": float("inf")}, {"cut_d": "2"}, {"radius": 0}, {"radius": -1},
            {"depth": 0}, {"depth": -1}, {"radius_1": 4}, {"zz": "invalid"}, {"mode": "invalid"},
        ):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                working.action(**({"radius": 5, "depth": 12, "mode": "true"} | overrides))
        with self.assertRaises(ValueError):
            working.action(cut_d=1)

    def test_anchors_rotation_and_inputs_are_preserved(self):
        for zz, z in (("center", -6), ("bottom", 0), ("top", -12)):
            kwargs = dict(radius=5, depth=12, cut_d=2, pos=[10, 20, 30], rot=[90, 0, 45], zz=zz, mode="true")
            original = copy.deepcopy(kwargs)
            result = working.action(**kwargs)[0]
            self.assertEqual(result["objects"][0]["pos"], [0, 0, z])
            self.assertEqual(result["pos"], [10, 20, 30])
            self.assertEqual(result["rot"], [90, 0, 45])
            self.assertEqual(kwargs, original)

    def test_dimension_aliases(self):
        for radius_arg in ({"r": 5}, {"diameter": 10}, {"d": 10}):
            for depth_arg in ({"depth_mm": 12}, {"h": 12}):
                obj = working.action(**radius_arg, **depth_arg, cut_d=2, mode="true")[0]["objects"][0]
                self.assertEqual((obj["r"], obj["h"]), (5, 12))

    def test_mode_aware_lookup_and_explicit_radius_precedence(self):
        radii = {"laser": 4.9, "3dpr": 5.2, "true": 5}
        with mock.patch.object(oobb, "gv", side_effect=lambda name, mode: radii[mode]):
            result = working.action(radius_name="test_radius", cut_d=2, depth=12)
        self.assertEqual([obj["inclusion"] for obj in result], list(radii))
        for obj in result:
            r = radii[obj["inclusion"]]
            self.assertEqual(obj["objects"][0]["r"], r)
            self.assertEqual(obj["objects"][1]["pos"][1], r - 2)
        with mock.patch.object(oobb, "gv") as lookup:
            working.action(radius=5, radius_name="ignored", mode="true")
            lookup.assert_not_called()

    def test_named_depth_resolved_before_anchoring(self):
        with mock.patch.object(oobb, "gv", return_value=12):
            obj = working.action(radius=5, depth="named_depth", mode="true")[0]["objects"][0]
        self.assertEqual((obj["h"], obj["pos"][2]), (12, -6))

    def test_public_dispatch_and_negative_geometry_render(self):
        shaft = oobb.oobb_easy(shape="oobb_cylinder_d_shaft", type="n", radius=5, cut_d=2, depth=12, mode="true", rot_z=90)
        self.assertEqual(shaft[0][0]["typetype"], "n")
        self.assertEqual(shaft[0][0]["rot"], [0, 0, 90])
        block = opsc.opsc_easy("p", "cube", size=[20, 20, 10], pos=[-10, -10, -5])
        scad = opsc.opsc_get_object([block] + shaft, mode="true").as_scad()
        self.assertIn("difference()", scad)
        self.assertIn("cylinder(h = 12, r = 5)", scad)

    def test_mode_filter_excludes_unselected_geometry(self):
        shaft = working.action(radius=5, cut_d=2, mode="3dpr")
        scad = opsc.opsc_get_object(shaft, mode="laser").as_scad()
        self.assertNotIn("cylinder(", scad)

    @unittest.skipUnless(shutil.which("openscad.com") or shutil.which("openscad"), "OpenSCAD required for mesh checks")
    def test_rendered_mesh_volume_and_flat_position(self):
        executable = shutil.which("openscad.com") or shutil.which("openscad")
        with tempfile.TemporaryDirectory() as tmp:
            for cut_d, negative in ((0, False), (1, False), (2, False), (5, False), (2, True)):
                with self.subTest(cut_d=cut_d, negative=negative):
                    shaft = working.action(radius=5, depth=12, cut_d=cut_d, type="n" if negative else "p", mode="true")
                    if negative:
                        shaft.insert(0, opsc.opsc_easy("p", "cube", size=[20, 20, 10], pos=[-10, -10, -5]))
                    source = Path(tmp) / "shaft.scad"
                    target = Path(tmp) / "shaft.stl"
                    source.write_text("$fn=200;\n" + opsc.opsc_get_object(shaft, mode="true").as_scad(), encoding="utf-8")
                    completed = subprocess.run([executable, "--export-format", "asciistl", "-o", str(target), str(source)], capture_output=True, text=True, timeout=60)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    vertices = [tuple(map(float, match)) for match in re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", target.read_text())]
                    self.assertTrue(vertices)
                    volume = 0
                    for i in range(0, len(vertices), 3):
                        a, b, c = vertices[i:i + 3]
                        volume += (a[0] * (b[1]*c[2] - b[2]*c[1]) + a[1] * (b[2]*c[0] - b[0]*c[2]) + a[2] * (b[0]*c[1] - b[1]*c[0])) / 6
                    flat_y = 5 - cut_d
                    removed_area = 25 * math.acos(flat_y / 5) - flat_y * math.sqrt(25 - flat_y**2)
                    remaining_area = 25 * math.pi - removed_area
                    expected_volume = 4000 - remaining_area * 10 if negative else remaining_area * 12
                    self.assertAlmostEqual(abs(volume), expected_volume, delta=expected_volume * 0.001)
                    if not negative:
                        self.assertAlmostEqual(max(v[1] for v in vertices), flat_y, places=4)
                        self.assertEqual((min(v[2] for v in vertices), max(v[2] for v in vertices)), (-6, 6))


if __name__ == "__main__":
    unittest.main()
