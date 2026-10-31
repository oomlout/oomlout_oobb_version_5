"""Cylinder with a flat specified by the material removed, in millimetres."""

import copy
import math
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def describe():
    global d
    d = {
        "name": "oobb_cylinder_d_shaft",
        "name_long": "OOBB Geometry Primitives: D-Shaft Cylinder",
        "description": "Cylinder with a flat cut from the +Y side. cut_d is the material removed in mm; the remaining flat-to-back size is 2 * radius - cut_d.",
        "category": "OOBB Geometry Primitives",
        "shape_aliases": [],
        "returns": "List of mode-specific rotation objects containing a cylinder minus a flat cut.",
        "variables": [
            {"name": "radius", "description": "Cylinder radius in mm; r is an alias. Supply a radius, diameter, or radius_name.", "type": "number", "default": "(required unless diameter or radius_name is supplied)"},
            {"name": "diameter", "description": "Cylinder diameter in mm; d is an alias. Explicit radius takes precedence.", "type": "number", "default": "(optional)"},
            {"name": "radius_name", "description": "Mode-aware OOBB radius lookup, used when no explicit radius or diameter is supplied.", "type": "string", "default": ""},
            {"name": "cut_d", "description": "Depth removed from the +Y curved edge in mm. Flat is at y = radius - cut_d before rotation. Must satisfy 0 <= cut_d < 2 * radius; 0 leaves a full cylinder.", "type": "number", "default": 1},
            {"name": "depth", "description": "Cylinder length along local Z in mm (aliases: depth_mm, h). May be an OOBB dimension name.", "type": "number or string", "default": 250},
            {"name": "pos", "description": "Anchor position [x,y,z] in mm.", "type": "list", "default": "[0,0,0]"},
            {"name": "zz", "description": "Local Z anchor: center, bottom, or top, applied before rotation.", "type": "string", "default": "center"},
            {"name": "type", "description": "p/positive for a solid shaft; n/negative for a D-shaped hole.", "type": "string", "default": "p"},
            {"name": "rot", "description": "Rotation [rx,ry,rz] in degrees about pos. Alternatively use rot_x, rot_y, rot_z.", "type": "list", "default": "[0,0,0]"},
            {"name": "mode", "description": "Render mode string or list: laser, 3dpr, true.", "type": "list or string", "default": '["laser","3dpr","true"]'},
        ],
    }
    return d


def define():
    if not d:
        describe()
    return dict(d)


def _finite_number(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number in mm")
    return value


def action(**kwargs):
    import oobb
    import opsc

    if any(key in kwargs for key in ("r1", "r2", "radius_1", "radius_2")):
        raise ValueError("oobb_cylinder_d_shaft requires a constant radius")
    cut_d = _finite_number("cut_d", kwargs.get("cut_d", 1))
    if cut_d < 0:
        raise ValueError("cut_d must be non-negative")
    zz = kwargs.get("zz", "center")
    if zz not in ("center", "bottom", "top"):
        raise ValueError("zz must be center, bottom, or top")
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    modes = [modes] if isinstance(modes, str) else list(modes)
    if not modes or any(mode not in ("laser", "3dpr", "true") for mode in modes):
        raise ValueError("mode must contain laser, 3dpr, or true")

    pos = copy.deepcopy(kwargs.get("pos", [kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("z", 0)]))
    rot = copy.deepcopy(kwargs.get("rot", ""))
    if rot == "":
        rot = [kwargs.get("rot_x", 0), kwargs.get("rot_y", 0), kwargs.get("rot_z", 0)]
    depth_input = kwargs.get("depth", kwargs.get("depth_mm", kwargs.get("h", 250)))

    result = []
    for mode in modes:
        if "radius" in kwargs or "r" in kwargs:
            radius = kwargs.get("radius", kwargs.get("r"))
        elif "diameter" in kwargs or "d" in kwargs:
            radius = _finite_number("diameter", kwargs.get("diameter", kwargs.get("d"))) / 2
        elif kwargs.get("radius_name"):
            radius = oobb.gv(kwargs["radius_name"], mode)
        else:
            raise ValueError("Supply radius/r, diameter/d, or radius_name")
        radius = _finite_number("radius", radius)
        depth = oobb.gv(depth_input, mode) if isinstance(depth_input, str) else depth_input
        depth = _finite_number("depth", depth)
        if radius <= 0 or depth <= 0:
            raise ValueError("radius and depth must be positive")
        if cut_d >= 2 * radius:
            raise ValueError(f"cut_d must be less than the diameter ({2 * radius} mm) in {mode} mode")

        z = {"center": -depth / 2, "bottom": 0, "top": -depth}[zz]
        objects = [opsc.opsc_easy("positive", "cylinder", r=radius, h=depth, pos=[0, 0, z])]
        if cut_d:
            # Extend beyond the cylinder on X/Z and +Y to avoid coincident faces.
            margin = 0.1
            objects.append(opsc.opsc_easy(
                "negative", "cube",
                size=[2 * radius + 2 * margin, cut_d + margin, depth + 2 * margin],
                pos=[-radius - margin, radius - cut_d, z - margin],
            ))
        result.append({
            "type": "rotation", "typetype": kwargs.get("type", "p"),
            "pos": copy.deepcopy(pos), "rot": copy.deepcopy(rot),
            "inclusion": mode, "objects": objects,
        })
    return result


def test():
    import opsc

    samples = [
        {"filename": "test_1", "kwargs": {"radius": 5, "depth": 12, "cut_d": 0, "mode": "true"}},
        {"filename": "test_2", "kwargs": {"radius": 5, "depth": 12, "cut_d": 1, "mode": "true"}},
        {"filename": "test_3", "kwargs": {"radius": 5, "depth": 12, "cut_d": 2, "mode": "true"}},
        {"filename": "test_4", "kwargs": {"radius": 5, "depth": 12, "cut_d": 5, "mode": "true"}},
    ]
    generated_files = []
    for sample in samples:
        sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test", sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        opsc.opsc_make_object(
            scad_path, action(**sample["kwargs"]), mode="true",
            save_type="none", overwrite=True, render=False,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(os.path.join(sample_dir, "image.png"))
    return generated_files
