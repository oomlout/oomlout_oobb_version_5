import re

import opsc
from components.oobb_surface import working


def test_multi_surface_design_keeps_every_generated_module(tmp_path):
    output_path = tmp_path / "working.scad"
    image_path = working._DEFAULT_IMAGE
    surfaces = [
        {
            "type": "positive",
            "shape": "oobb_surface",
            "file": image_path,
            "width": 30,
            "depth": 1,
            "pos": [-20, 0, 0],
        },
        {
            "type": "positive",
            "shape": "oobb_surface",
            "file": image_path,
            "width": 45,
            "depth": 2,
            "pos": [20, 0, 0],
        },
    ]

    opsc.opsc_make_object(
        str(output_path),
        surfaces,
        mode="true",
        save_type="none",
        overwrite=True,
        render=False,
    )

    generated_modules = sorted(tmp_path.glob("oobb_surface_*.scad"))
    assert len(generated_modules) == 2

    design_scad = output_path.read_text(encoding="utf-8")
    used_modules = set(re.findall(r"use <(oobb_surface_[0-9a-f]{12}\.scad)>;", design_scad))
    assert used_modules == {path.name for path in generated_modules}
