import copy
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import oobb
import opsc
from components.oobb_gear_bevel import working


class BevelGearTests(unittest.TestCase):
    def test_public_dispatch_modes_and_transforms(self):
        kwargs = dict(shape="oobb_gear_bevel", teeth=50, mod=0.75, depth=6,
                      mode=["3dpr", "true"], pos=[8, 9, 10], rot=[90, 0, 15])
        original = copy.deepcopy(kwargs)
        result = oobb.oobb_easy(**kwargs)
        for mode in ("3dpr", "true"):
            scad = opsc.opsc_get_object(result, mode=mode).as_scad()
            self.assertIn("oobb_gear_bevel_raw(", scad)
            self.assertIn("translate(v = [8, 9, 10])", scad)
            self.assertIn("rotate(a = [90, 0, 15])", scad)
        self.assertNotIn("oobb_gear_bevel_raw(", opsc.opsc_get_object(result, mode="laser").as_scad())
        self.assertEqual(kwargs, original)

    def test_invalid_geometry_fails_early(self):
        for values in (
            {"teeth": 2}, {"teeth": 20.5}, {"mate_teeth": True},
            {"mod": 0}, {"depth": float("nan")}, {"shaft_angle": 80},
            {"face_width": 100}, {"face_width": 0}, {"teeth":20,"mod":0.75,"depth":12},
            {"shaft_diam": 50}, {"pressure_angle": 90}, {"backlash": 5},
            {"clearance": -1}, {"anchor": "invalid"}, {"gear_spin": float("inf")},
            {"mode": []}, {"mode": "other"},
            {"base_chamfer": -0.1}, {"base_chamfer": 10},
            {"underside_angle": 44}, {"underside_angle": 90},
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                working.action(**values)

    def test_ratio_and_safe_face_width(self):
        small = working.dimensions(teeth=20, mate_teeth=40)
        large = working.dimensions(teeth=40, mate_teeth=20)
        self.assertAlmostEqual(small["pitch_angle"] + large["pitch_angle"], 90)
        self.assertAlmostEqual(small["cone_distance"], large["cone_distance"])
        self.assertLess(small["face_width"], small["cone_distance"])

    @unittest.skipUnless(shutil.which("openscad.com") or shutil.which("openscad"), "OpenSCAD required")
    def test_mesh_envelope_bore_and_anchors(self):
        import trimesh

        executable = shutil.which("openscad.com") or shutil.which("openscad")
        with tempfile.TemporaryDirectory() as tmp:
            for anchor, expected, chamfer in (("center", (-3, 3), 0.4), ("bottom", (0, 6), 0)):
                with self.subTest(anchor=anchor):
                    source = Path(tmp) / f"{anchor}.scad"
                    mesh_path = source.with_suffix(".stl")
                    objects = working.action(teeth=50, mod=0.75, depth=6, shaft_diam=3.6, anchor=anchor, base_chamfer=chamfer)
                    opsc.opsc_make_object(str(source), objects, mode="3dpr", save_type="none", render=False)
                    proc = subprocess.run([executable, "--hardwarnings", "-o", str(mesh_path), str(source)],
                                          capture_output=True, text=True, timeout=60)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    mesh = trimesh.load(mesh_path)
                    self.assertTrue(mesh.is_watertight)
                    self.assertEqual(len(mesh.split()), 1)
                    self.assertAlmostEqual(mesh.bounds[0, 2], expected[0], places=5)
                    self.assertAlmostEqual(mesh.bounds[1, 2], expected[1], places=5)
                    # No mesh vertices intrude into the polygonal shaft bore.
                    radial_distance = (mesh.vertices[:, 0]**2 + mesh.vertices[:, 1]**2)**0.5
                    self.assertGreaterEqual(radial_distance.min(), 1.8 * math.cos(math.pi/12) - 1e-5)
                    near_bore = mesh.vertices[radial_distance < 1.85]
                    self.assertAlmostEqual(near_bore[:,2].max(), expected[1], places=5)
                    centers=mesh.triangles_center
                    downward=(centers[:,2]>expected[0]+0.01)&(mesh.face_normals[:,2]<-0.01)
                    angles=[math.degrees(math.acos(-z)) for z in mesh.face_normals[downward,2]]
                    self.assertTrue(angles)
                    self.assertGreaterEqual(min(angles),44.9)
                    if chamfer:
                        radii=[]
                        for h in (0.05,0.15):
                            section=mesh.section(plane_origin=[0,0,expected[0]+h],plane_normal=[0,0,1])
                            outer=max(section.discrete,key=lambda p:max(math.hypot(v[0],v[1]) for v in p))
                            ring=[math.hypot(p[0],p[1]) for p in outer]
                            self.assertLess(max(ring)-min(ring),max(ring)*0.002+1e-4,
                                            "Teeth must not reach the bed footprint")
                            radii.append(max(ring))
                        self.assertAlmostEqual(radii[1]-radii[0],0.1,delta=0.002,
                                               msg="The body must start on a 45 degree ramp, without a vertical pedestal")


if __name__ == "__main__":
    unittest.main()
