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
    d = {}
    d["name"] = "pulley_gt2"
    d["name_long"] = "OPSC Mechanical Shapes: GT2 Pulley"
    d["description"] = "GT2 2 mm tooth profile with explicit fit allowances and no implicit shaft bore."
    d["category"] = "OPSC Mechanical Shapes"
    d["shape_aliases"] = ["pulley_gt2"]
    d["returns"] = "List of geometry component dicts."
    d["variables"] = [
        {"name": "number_of_teeth", "type": "number", "default": 24, "description": "Integer tooth count, at least 8."},
        {"name": "depth", "type": "number", "default": 6, "description": "Toothed length, bottom anchored, in mm."},
        {"name": "additional_tooth_width", "type": "number", "default": 0.2, "description": "Extra tooth pocket width in mm."},
        {"name": "additional_tooth_depth", "type": "number", "default": 0, "description": "Extra tooth pocket depth in mm."},
    ]
    return d


def define():
    global d
    if not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def action(**kwargs):
    import opsc

    params = copy.deepcopy(kwargs)
    params.setdefault("type", "positive")
    params["shape"] = "pulley_gt2"
    teeth = params.get("number_of_teeth", 24)
    if isinstance(teeth, bool) or not isinstance(teeth, (int, float)) or not math.isfinite(teeth) or teeth < 8 or int(teeth) != teeth:
        raise ValueError("number_of_teeth must be an integer of at least 8")
    depth = params.get("depth", 6)
    if isinstance(depth, bool) or not isinstance(depth, (int, float)) or not math.isfinite(depth) or depth <= 0:
        raise ValueError("depth must be a positive finite number")
    result = opsc.opsc_easy(**params)
    # Preserve component keywords without changing the OPSC global whitelist.
    for name, default, maximum in [("additional_tooth_width", 0.2, 0.5), ("additional_tooth_depth", 0, 0.3)]:
        value = params.get(name, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= maximum:
            raise ValueError(f"{name} must be between zero and {maximum}")
        result[name] = value
    return [result]


def _resolve_scad_asset(filename):
    root_candidate = os.path.join(_PROJECT_ROOT, filename)
    if os.path.exists(root_candidate):
        return root_candidate

    reference_candidate = os.path.join(_PROJECT_ROOT, "reference", "oomlout_opsc_version_3", filename)
    if os.path.exists(reference_candidate):
        return reference_candidate

    return filename


def render(params):
    from solid2 import import_scad

    pulley_scad = import_scad(_resolve_scad_asset("pulley_gt2.scad"))
    return pulley_scad.pulley_gt2(
        number_of_teeth=params.get("number_of_teeth", 24),
        depth=params.get("depth", 6),
        tooth_width_clearance=params.get("additional_tooth_width", 0.2),
        tooth_depth_clearance=params.get("additional_tooth_depth", 0),
    )


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [70, 0, 20],
      'kwargs': {'type': 'positive', 'number_of_teeth': 16, 'depth': 6, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [70, 0, 20],
      'kwargs': {'type': 'positive', 'number_of_teeth': 20, 'depth': 7, 'pos': [0, 0, 0]}}]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

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


