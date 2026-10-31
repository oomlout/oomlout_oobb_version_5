"""Flush SVG inlays on cylinder end faces, with complementary colour solids."""
import copy
import math
import sys
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def describe():
    return {
        "name": "oobb_cylinder_inlay",
        "name_long": "OOBB Geometry Primitives: Cylinder with SVG Inlay",
        "description": "Complementary flush end-face SVG inlays, optionally clipped to an existing drilled cylinder body.",
        "category": "OOBB Geometry Primitives",
        "shape_aliases": [],
        "returns": "List of mode-specific geometry dictionaries; select base, inlay or combined for export.",
        "variables": [
            {"name": name, "description": description, "type": typ, "default": default}
            for name, description, typ, default in [
                ("radius", "Cylinder radius in mm; r/diameter/d/radius_name also accepted.", "number", 10),
                ("depth", "Length along local Z in mm; depth_mm/h also accepted.", "number", 10),
                ("zz", "Local anchor: center, bottom or top, applied before rot/pos.", "string", "center"),
                ("svg", "SVG file; use filled paths with text converted to paths and physical mm dimensions.", "string", ""),
                ("svg_bottom", "Optional different artwork for the bottom face.", "string", "same as svg"),
                ("inlay", "False returns the plain body without requiring an SVG.", "bool", True),
                ("inlay_depth", "Flush material depth in mm; both faces must not overlap.", "number", 0.84),
                ("inlay_face", "top, bottom or both; viewed from outside each face.", "string", "top"),
                ("part", "base subtracts inlay, inlay returns accent only, combined colours both.", "string", "base"),
                ("mirror", "Reflect placed artwork horizontally about the face origin in its outward view.", "bool", False),
                ("svg_center", "Centre imported SVG using OpenSCAD's import center option.", "bool", True),
                ("svg_scale", "Uniform scale or [sx,sy] in artwork coordinates.", "number or list", 1),
                ("svg_rotate", "Artwork rotation in degrees before offset.", "number", 0),
                ("svg_offset", "[x,y] offset after scaling and rotation in the outward face view.", "list", "[0,0]"),
                ("body_components", "Optional OOBB body components in cylinder-local coordinates; retains holes and fits.", "list", "[]"),
                ("base_color", "Combined-preview body colour.", "string", "#008C95"),
                ("inlay_color", "Combined-preview inlay colour.", "string", "#FFD52A"),
            ]
        ],
    }


def define():
    return describe()


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


def action(**kwargs):
    import oobb
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    modes = [modes] if isinstance(modes, str) else list(modes)
    if not modes or any(mode not in ("laser", "3dpr", "true") for mode in modes):
        raise ValueError("mode must contain laser, 3dpr or true")
    if kwargs.get("part", "base") not in ("base", "inlay", "combined"):
        raise ValueError("part must be base, inlay or combined")
    if kwargs.get("inlay_face", "top") not in ("top", "bottom", "both"):
        raise ValueError("inlay_face must be top, bottom or both")
    if kwargs.get("zz", "center") not in ("center", "top", "bottom"):
        raise ValueError("zz must be center, top or bottom")
    if kwargs.get("inlay", True):
        for name in ("svg", "svg_bottom"):
            filename = kwargs.get(name, kwargs.get("svg"))
            if not filename or not Path(filename).is_file() or Path(filename).suffix.lower() != ".svg":
                raise ValueError(f"{name} must reference an existing SVG file")
    result = []
    for mode in modes:
        p3 = copy.deepcopy(kwargs)
        radius = kwargs.get("radius", kwargs.get("r"))
        if radius is None and ("diameter" in kwargs or "d" in kwargs):
            radius = _number(kwargs.get("diameter", kwargs.get("d")), "diameter") / 2
        if radius is None and kwargs.get("radius_name"):
            radius = oobb.gv(kwargs["radius_name"], mode)
        radius = _number(radius, "radius")
        depth = kwargs.get("depth", kwargs.get("depth_mm", kwargs.get("h", 10)))
        depth = oobb.gv(depth, mode) if isinstance(depth, str) else depth
        depth = _number(depth, "depth")
        inlay_depth = _number(kwargs.get("inlay_depth", .84), "inlay_depth")
        faces = 2 if kwargs.get("inlay_face", "top") == "both" else 1
        if radius <= 0 or depth <= 0:
            raise ValueError("radius and depth must be positive")
        if kwargs.get("inlay", True) and not 0 < inlay_depth * faces < depth:
            raise ValueError("Inlay depth must be positive and leave body material between the faces")
        p3["shape"] = "oobb_cylinder_inlay"
        p3["radius"] = radius
        p3["depth"] = depth
        p3["inlay_depth"] = inlay_depth
        p3["type"] = kwargs.get("type", "positive")
        p3["pos"] = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
        p3["rot"] = copy.deepcopy(kwargs.get("rot", [0, 0, 0]))
        p3["inclusion"] = mode
        result.append(p3)
    return result


def render(params):
    import opsc
    from solid2 import color, cylinder, difference, import_, intersection, linear_extrude, mirror, rotate, scale, translate, union
    depth = params["depth"]
    z = {"center": -depth / 2, "bottom": 0, "top": -depth}[params.get("zz", "center")]
    envelope = translate([0, 0, z])(cylinder(r=params.get("radius", params.get("r")), h=depth))
    body = envelope
    if params.get("body_components"):
        body = opsc.opsc_get_object(copy.deepcopy(params["body_components"]), mode=params["inclusion"])
    if not params.get("inlay", True):
        return body if params.get("part", "base") != "inlay" else union()()
    pieces = []
    for face in ("top", "bottom"):
        if params.get("inlay_face", "top") not in (face, "both"):
            continue
        svg = params.get("svg_bottom", params["svg"]) if face == "bottom" else params["svg"]
        art = import_(file=str(Path(svg).resolve()).replace("\\", "/"))
        # SolidPython's older import_ signature predates SVG's centre option.
        art._params["center"] = params.get("svg_center", True)
        size = params.get("svg_scale", 1)
        size = [size, size] if isinstance(size, (int, float)) else size
        art = translate(params.get("svg_offset", [0, 0]))(rotate(params.get("svg_rotate", 0))(scale(size)(art)))
        if params.get("mirror", False):
            art = mirror([1, 0, 0])(art)
        # The bottom view has its horizontal axis reversed relative to local XY.
        if face == "bottom":
            art = mirror([1, 0, 0])(art)
        height = params["inlay_depth"]
        level = z + depth - height if face == "top" else z
        pieces.append(translate([0, 0, level])(linear_extrude(height=height)(art)))
    accent = intersection()(body, envelope, union()(*pieces))
    base = difference()(body, accent)
    if params.get("part", "base") == "inlay":
        return accent
    if params.get("part", "base") == "combined":
        return union()(color(params.get("base_color", "#008C95"))(base), color(params.get("inlay_color", "#FFD52A"))(accent))
    return base
