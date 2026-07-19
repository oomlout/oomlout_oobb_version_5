import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from solidpython_compat import apply_modifier

d = {}


def describe():
    global d
    d = {}
    d["name"] = "sphere_cylinder"
    d["name_long"] = "OPSC Composite Shapes: Sphere Cylinder"
    d["description"] = "Cylinder with rounded top and bottom outside edges, intended as a drop-in rounded replacement for cylinder."
    d["category"] = "OPSC Composite Shapes"
    d["shape_aliases"] = ["sphere_cylinder"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "r", "description": "Outer cylinder radius in mm.", "type": "number", "default": 1})
    v.append({"name": "h", "description": "Cylinder height in mm.", "type": "number", "default": 1})
    v.append({"name": "radius_rounded", "description": "Rounded edge radius in mm.", "type": "number", "default": 1})
    v.append({"name": "center", "description": "Match OpenSCAD cylinder center behaviour.", "type": "boolean", "default": False})
    d["variables"] = v
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
    params["shape"] = "sphere_cylinder"
    return [opsc.opsc_easy(**params)]


def _get_height(params):
    return params.get("h", params.get("height", params.get("depth", 1)))


def _get_radius(params):
    if "r" in params:
        return params["r"]
    if "radius" in params:
        return params["radius"]
    if "d" in params:
        return params["d"] / 2
    if "diameter" in params:
        return params["diameter"] / 2
    return None


def _get_tapered_radii(params):
    r1 = params.get("r1", params.get("radius_1", None))
    r2 = params.get("r2", params.get("radius_2", None))
    return r1, r2


def _plain_cylinder(params):
    from solid2 import cylinder

    height = _get_height(params)
    shape_params = {"h": height, "center": params.get("center", False)}
    radius = _get_radius(params)
    r1, r2 = _get_tapered_radii(params)
    base_radius = radius if radius is not None else 1

    if r1 is not None or r2 is not None:
        shape_params["r1"] = r1 if r1 is not None else base_radius
        shape_params["r2"] = r2 if r2 is not None else base_radius
    elif "d" in params:
        shape_params["d"] = params["d"]
    elif "diameter" in params:
        shape_params["d"] = params["diameter"]
    else:
        shape_params["r"] = radius if radius is not None else 1

    return cylinder(**shape_params)


def render(params):
    import opsc
    from solid2 import union

    m = params.get("m", "")
    height = _get_height(params)
    radius = _get_radius(params)
    r1, r2 = _get_tapered_radii(params)

    if height <= 0 or radius is None or radius <= 0:
        return apply_modifier(_plain_cylinder(params), m)

    if (r1 is not None or r2 is not None) and r1 != r2:
        return apply_modifier(_plain_cylinder(params), m)

    radius_rounded = params.get("radius_rounded", params.get("r_rounded", 1))
    radius_rounded = min(radius_rounded, height / 2, radius / 2)
    if radius_rounded <= 0:
        return apply_modifier(_plain_cylinder(params), m)

    z_offset = -height / 2 if params.get("center", False) else 0
    middle_height = max(height - radius_rounded * 2, 0)
    inner_radius = max(radius - radius_rounded, 0)
    oring_id = max(radius - radius_rounded * 2, 0)

    children = []

    if inner_radius > 0:
        inset_cylinder = {
            "type": "positive",
            "shape": "cylinder",
            "r": inner_radius,
            "h": height,
            "pos": [0, 0, z_offset],
            "m": "",
        }
        children.append(opsc.get_opsc_item(inset_cylinder))

    if middle_height > 0:
        middle_cylinder = {
            "type": "positive",
            "shape": "cylinder",
            "r": radius,
            "h": middle_height,
            "pos": [0, 0, z_offset + radius_rounded],
            "m": "",
        }
        children.append(opsc.get_opsc_item(middle_cylinder))

    for z_pos in [z_offset + radius_rounded, z_offset + height - radius_rounded]:
        edge_round = {
            "type": "positive",
            "shape": "oring",
            "id": oring_id,
            "depth": radius_rounded * 2,
            "pos": [0, 0, z_pos],
            "m": "",
        }
        children.append(opsc.get_opsc_item(edge_round))

    return apply_modifier(union()(*children), m)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'r': 8, 'h': 20, 'radius_rounded': 2, 'pos': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'diameter': 18, 'depth': 12, 'radius_rounded': 3, 'pos': [0, 0, 0]}},
     {'filename': 'test_3',
      'preview_rot': [45, 0, 25],
      'kwargs': {'type': 'positive', 'r': 8, 'h': 20, 'radius_rounded': 2, 'center': True, 'pos': [0, 0, 0]}}]

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
