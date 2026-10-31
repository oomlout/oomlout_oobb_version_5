"""Check the printed footprint, closed floor, and component dispatch."""

import shutil
import subprocess
from pathlib import Path

import pytest

from components.gridfinity_tray_quarter_increment import working as quarter


@pytest.mark.parametrize("width,height", [(0.75, 0.75), (0.25, 1.25), (0.3, 1), (0, 1)])
def test_unsupported_dimensions_fail(width, height):
    with pytest.raises(ValueError):
        quarter.action(width=width, height=height)


def test_oobb_dispatch_and_dimension_aliases():
    import oobb

    geometry = oobb.oe(
        shape="gridfinity_tray_quarter_increment",
        gridfinity_width=[0, 31.5], height=0.5, depth=18 / 7,
        pos=[10, 20, 30], rot=[0, 0, 90],
    )[0][0]
    assert geometry["module"] == "gridfinity_tray_quarter_increment"
    assert geometry["pos"] == [10, 20, 30]
    assert geometry["rot"] == [0, 0, 90]
    assert geometry["module_kwargs"]["gridfinity_width"] == [0, 31.5]
    assert geometry["module_kwargs"]["gridfinity_height"] == 0.5
    assert geometry["module_kwargs"]["efficient_floor"] == "on"
    assert quarter.action(width=0.75, height=1, efficient_floor="off")["module_kwargs"]["efficient_floor"] == "off"


@pytest.mark.parametrize("width,height,feet", [
    (0.75, 1, [(0.5, 1), (0.25, 1)]),
    (1, 0.75, [(1, 0.5), (1, 0.25)]),
    (0.75, 0.5, [(0.5, 0.5), (0.25, 0.5)]),
    (0.5, 0.25, [(0.5, 0.25)]),
    (1.25, 1, [(1, 1), (0.25, 1)]),
    (1, 1.75, [(1, 1), (1, 0.5), (1, 0.25)]),
    (3, 0.75, [(1, 0.5), (1, 0.25)] * 3),
])
@pytest.mark.parametrize("floor_style", ["on", "off"])
def test_rendered_feet_and_closed_floor(tmp_path, width, height, feet, floor_style):
    trimesh = pytest.importorskip("trimesh")
    np = pytest.importorskip("numpy")
    openscad = shutil.which("openscad.com") or shutil.which("openscad")
    if not openscad:
        pytest.skip("OpenSCAD is not installed")
    source = tmp_path / "tray.scad"
    output = tmp_path / "tray.stl"
    wrapper = Path(quarter._WRAPPER_FILE).as_posix()
    source.write_text(f'''use <{wrapper}>;
gridfinity_tray_quarter_increment(
    gridfinity_width={width}, gridfinity_height={height}, gridfinity_depth=18/7,
    wall_thickness=1.25, lip_style="none", efficient_floor="{floor_style}", fn=32);
''', encoding="utf-8")
    result = subprocess.run(
        [openscad, "--backend=Manifold", "-o", str(output), str(source)],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR:" not in result.stdout + result.stderr
    mesh = trimesh.load(output)
    assert mesh.is_watertight
    assert len(mesh.split()) == 1
    assert mesh.euler_number == 2  # A cup with no accidental hole through its floor.
    assert mesh.extents[:2] == pytest.approx([width * 42 - 0.5, height * 42 - 0.5])
    # At z=2, the standard profile is inset 2.4 mm from each cell edge.
    section = mesh.section(plane_origin=[0, 0, 2], plane_normal=[0, 0, 1])
    actual = sorted(tuple(np.round(np.ptp(loop, axis=0)[:2], 3)) for loop in section.discrete)
    expected = sorted((round(x * 42 - 4.8, 3), round(y * 42 - 4.8, 3)) for x, y in feet)
    assert sorted(size for size in actual if size in expected) == expected
    # Each recessed foot has an inner contour at z=2, above its thin closed floor.
    assert len(actual) == len(feet) * (2 if floor_style == "on" else 1)
    below_floor = mesh.section(plane_origin=[0, 0, 0.35], plane_normal=[0, 0, 1])
    assert len(below_floor.discrete) == len(feet)
    upward_faces = mesh.triangles_center[mesh.face_normals[:, 2] > 0.999]
    assert upward_faces[:, 2].min() == pytest.approx(0.71 if floor_style == "on" else 5.7, abs=0.001)
    # Feet join one body; the efficient floor opens down into each individual foot.
    floor = mesh.section(plane_origin=[0, 0, 5.2], plane_normal=[0, 0, 1])
    assert len(floor.discrete) == (1 + len(feet) if floor_style == "on" else 1)
