import shutil
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRAY_WRAPPERS = [
    PROJECT_ROOT / "components" / component / "gridfinity_tray_raw_wrapper.scad"
    for component in (
        "gridfinity_tray_raw",
        "gridfinity_tray_default",
        "gridfinity_tray_default_label",
        "gridfinity_tray_fractional_test",
    )
]


@pytest.mark.parametrize("wrapper", TRAY_WRAPPERS, ids=lambda path: path.parent.name)
def test_half_unit_dimensions_select_half_pitch_squares(wrapper, tmp_path):
    openscad = shutil.which("openscad.com") or shutil.which("openscad")
    if openscad is None:
        pytest.skip("OpenSCAD is not installed")

    wrapper_path = wrapper.as_posix()
    source = tmp_path / "fractional_bottom_pattern.scad"
    source.write_text(
        f"""
use <{wrapper_path}>

pitch = [42, 42, 7];

assert(_gridfinity_effective_sub_pitch(0.5, 1, 1, pitch) == 2);
assert(_gridfinity_effective_sub_pitch(2.5, 1, 1, pitch) == 2);
assert(_gridfinity_effective_sub_pitch(2, 1.5, 1, pitch) == 2);
assert(_gridfinity_effective_sub_pitch([2, 21], 1, 1, pitch) == 2);
assert(_gridfinity_effective_sub_pitch(2, 1, 1, pitch) == 1);
assert(_gridfinity_effective_sub_pitch(2, 1, 3, pitch) == 3);

gridfinity_tray_raw(
    gridfinity_width = 2.5,
    gridfinity_height = 1,
    gridfinity_depth = 1,
    pitch = pitch,
    force_render = false
);
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [openscad, "-o", str(tmp_path / "fractional_bottom_pattern.csg"), str(source)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
