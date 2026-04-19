import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_hole'
    d["name_long"] = 'OOBB Geometry Primitives: Hole (legacy)'
    d["description"] = 'Cylindrical screw hole for all render modes, resolved from a named or explicit radius.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['oobb_hole', 'hole']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'depth', "description": 'Hole depth in mm.', "type": 'number', "default": 200})
    v.append({"name": 'radius_name', "description": 'Named radius key, e.g. m3, m6.  Takes priority over radius.', "type": 'string', "default": '""'})
    v.append({"name": 'radius', "description": 'Explicit radius in mm, used when radius_name is empty.', "type": 'number', "default": 0})
    v.append({"name": 'r', "description": 'Alias for radius.', "type": 'number', "default": 0})
    v.append({"name": 'mode', "description": 'Render modes to emit: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
    v.append({"name": 'm', "description": 'OpenSCAD modifier prefix, e.g. #, %, *.', "type": 'string', "default": '""'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


def action(**kwargs):
    import oobb
    import opsc
    """Cylindrical hole for all three render modes, radius resolved by name or explicit value."""
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    modes = kwargs.get("mode", ["laser", "3dpr", "true"])
    if modes == "all":
        modes = ["laser", "3dpr", "true"]
    if isinstance(modes, str):
        modes = [modes]

    depth = kwargs.get("depth", 200)
    # Centre the hole vertically when no explicit depth was given
    if "depth" not in kwargs:
        pos[2] = pos[2] - depth / 2
    kwargs["pos"] = pos

    radius_name = kwargs.get("radius_name", "")
    r_fallback = kwargs.get("radius", kwargs.get("r", 0))

    typ = kwargs.get("type", "negative")

    return_value = []
    for mode in modes:
        p = copy.deepcopy(kwargs)
        p["inclusion"] = mode
        p["type"] = typ
        p["shape"] = "cylinder"
        p["h"] = depth
        if radius_name:
            try:
                p["r"] = oobb.gv("hole_radius_" + radius_name, mode)
            except Exception:
                p["r"] = oobb.gv(radius_name, mode)
        else:
            p["r"] = r_fallback
        return_value.append(opsc.opsc_easy(**p))

    return return_value
