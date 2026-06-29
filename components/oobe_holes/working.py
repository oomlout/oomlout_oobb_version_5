import copy
import importlib.util
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def _load_oobb_holes():
    path = os.path.join(_PROJECT_ROOT, "components", "oobb_holes", "working.py")
    spec = importlib.util.spec_from_file_location("comp_oobb_holes", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def describe():
    global d
    d = {}
    d["name"] = "oobe_holes"
    d["name_long"] = "OOBB Geometry Helpers: OOBE Hole Array (M3, 7.5 mm)"
    d["description"] = (
        "M3 screw holes on the OOBE 7.5 mm half-grid. "
        "Identical patterns to oobb_holes but spacing is fixed at 7.5 mm "
        "and hole size is fixed at M3. No both_holes option — there is no smaller grid."
    )
    d["category"] = "OOBB Geometry Helpers"
    d["shape_aliases"] = ["oobe_holes"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "holes",  "description": 'Hole pattern or list of patterns. Same values as oobb_holes: `all`, `perimeter`, `perimeter_miss_middle`, `u`, `top`, `bottom`, `left`, `right`, `corners`, `single`, `missing_middle`, `just_middle`, `circle`.', "type": "list",   "default": '["all"]'})
    v.append({"name": "width",  "description": "Width of the hole grid in OOBE units (each unit = 7.5 mm).",  "type": "number", "default": 0})
    v.append({"name": "height", "description": "Height of the hole grid in OOBE units (each unit = 7.5 mm).", "type": "number", "default": 0})
    v.append({"name": "pos",    "description": "Base position [x, y, z] in mm.",                             "type": "list",   "default": "[0,0,0]"})
    v.append({"name": "depth",  "description": "Hole depth in mm.",                                           "type": "number", "default": 100})
    v.append({"name": "middle", "description": "Include the centre hole for patterns that have one.",         "type": "bool",   "default": True})
    v.append({"name": "circle", "description": "Filter an `all` grid to only holes inside a circular boundary.", "type": "bool", "default": False})
    v.append({"name": "diameter", "description": "Circular pattern diameter in OOBE units.",                  "type": "number", "default": 0})
    v.append({"name": "diameter_clearance", "description": "Edge clearance in mm for circular filtering.",    "type": "number", "default": 7.5})
    v.append({"name": "diameter_center_clearance", "description": "Min distance from centre in mm before a hole is allowed.", "type": "number", "default": 0})
    v.append({"name": "loc",    "description": 'Grid location(s) for the `single` pattern. 1-based [x,y], e.g. `loc=[1,1]` or `loc=[[1,1],[3,2]]`.', "type": "list", "default": "[0,0]"})
    v.append({"name": "donut",  "description": "When True, use the circle approach — holes fill a ring. Requires `diameter` to set the outer size.", "type": "bool",   "default": False})
    v.append({"name": "diameter_center", "description": "Diameter of the hole-free zone in the centre, in OOBE units (each unit = 7.5 mm). Only used when `donut=True`.", "type": "number", "default": 0})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def action(**kwargs):
    oobb_holes = _load_oobb_holes()
    params = copy.deepcopy(kwargs)
    params["size"] = "oobe"
    params["radius_name"] = "m3"
    params.pop("both_holes", None)
    return oobb_holes.action(**params)


def test():
    import copy
    import os
    import opsc

    folder   = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        {
            "filename":    "test_1",
            "preview_rot": [60, 0, 25],
            "kwargs": {
                "holes":  ["all"],
                "width":  4,
                "height": 3,
                "pos":    [0, 0, 0],
                "depth":  6,
            },
        },
        {
            "filename":    "test_2",
            "preview_rot": [60, 0, 25],
            "kwargs": {
                "holes":  ["perimeter"],
                "width":  5,
                "height": 4,
                "pos":    [0, 0, 0],
                "depth":  6,
            },
        },
    ]

    generated_files = []

    for sample in samples:
        kwargs     = copy.deepcopy(sample["kwargs"])
        result     = action(**kwargs)
        components = result if isinstance(result, list) else [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path  = os.path.join(sample_dir, "working.scad")
        png_path   = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files
