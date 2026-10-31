"""Mesh-level contracts for complementary SVG colour exports."""
import copy
import shutil
import subprocess
from pathlib import Path
import numpy as np
import pytest
import oobb
import opsc
import trimesh
from components.oobb_cylinder_inlay import working


@pytest.fixture
def artwork(tmp_path):
    path = tmp_path/"asymmetric.svg"
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="20mm" height="20mm" viewBox="0 0 20 20"><path d="M 12,6 L 16,6 L 16,9 L 12,9 Z"/></svg>')
    return path


def test_rejects_missing_art_and_impossible_inlay(artwork):
    for overrides in [dict(svg="missing.svg"), dict(radius=-1), dict(inlay_depth=0),
                      dict(inlay_depth=5, inlay_face="both"), dict(depth=float("nan")),
                      dict(part="bad"), dict(zz="bad"), dict(mode="bad")]:
        with pytest.raises(ValueError):
            working.action(**(dict(radius=10, depth=10, svg=str(artwork)) | overrides))
    assert working.action(radius=10, depth=10, inlay=False)


def test_dispatch_preserves_input_and_resolves_modes(artwork):
    args = dict(shape="oobb_cylinder_inlay", radius=10, depth=10, svg=str(artwork),
                type="negative", pos=[1, 2, 3], rot=[90, 0, 0])
    before = copy.deepcopy(args)
    thing = dict(components=[], components_objects=[], components_string=[])
    oobb.append_full(thing, **args)
    assert args == before
    assert {p["inclusion"] for group in thing["components"] for p in group} == {"laser", "3dpr", "true"}
    assert "linear_extrude" in opsc.opsc_get_object(thing["components"], mode="3dpr").as_scad()


def test_mesh_complement_mirror_opposite_face_and_body_hole(artwork, tmp_path):
    executable = shutil.which("openscad.com") or shutil.which("openscad")
    if not executable:
        pytest.skip("OpenSCAD required")
    hole = opsc.opsc_easy("negative", "cylinder", r=1, h=12, pos=[4, 2.5, -6])
    body = [opsc.opsc_easy("positive", "cylinder", r=10, h=10, pos=[0, 0, -5]), hole]

    def export(name, **overrides):
        args = dict(radius=10, depth=10, svg=str(artwork), svg_center=False,
                    svg_offset=[-10, -10], mode="3dpr", inlay_depth=.84, body_components=body)
        args.update(overrides)
        source = tmp_path/(name+".scad")
        opsc.opsc_make_object(str(source), working.action(**args), mode="3dpr", save_type="none", overwrite=True)
        result = subprocess.run([executable, "--backend=Manifold", "-o", str(source.with_suffix(".stl")), str(source)], capture_output=True, text=True)
        assert result.returncode == 0 and "WARNING:" not in result.stderr and "ERROR:" not in result.stderr, result.stderr
        mesh = trimesh.load_mesh(source.with_suffix(".stl"))
        assert mesh.is_watertight and mesh.is_volume
        return mesh

    base = export("base", part="base")
    accent = export("accent", part="inlay")
    plain = export("plain", inlay=False)
    combined = trimesh.boolean.union([base, accent], engine="manifold")
    for a, b in [(combined, plain), (plain, combined)]:
        diff = trimesh.boolean.difference([a, b], engine="manifold")
        assert diff.is_empty or abs(diff.volume) < .001
    overlap = trimesh.boolean.intersection([base, accent], engine="manifold")
    assert overlap.is_empty or abs(overlap.volume) < .001
    assert np.allclose(accent.bounds[:, 2], [4.16, 5])
    assert accent.center_mass[0] > 0
    mirrored = export("mirrored", part="inlay", mirror=True)
    assert mirrored.center_mass[0] < 0
    # An asymmetric glyph is readable from the opposite outside viewpoint.
    bottom = export("bottom", part="inlay", inlay_face="bottom", zz="center")
    assert bottom.center_mass[0] < 0
    assert np.allclose(bottom.bounds[:, 2], [-5, -4.16])
    anchored = export("anchored", part="inlay", body_components=[], zz="bottom", rot=[90, 0, 0], pos=[1, 2, 3])
    assert np.allclose(anchored.bounds[:, 1], [-8, -7.16])
