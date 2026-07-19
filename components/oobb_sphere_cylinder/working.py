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
    d["name"] = "oobb_sphere_cylinder"
    d["name_long"] = "OOBB Geometry Primitives: Sphere Cylinder"
    d["description"] = "OOBB cylinder wrapper that can emit either a normal cylinder or the rounded sphere_cylinder shape."
    d["category"] = "OOBB Geometry Primitives"
    d["shape_aliases"] = ["oobb_sphere_cylinder"]
    d["returns"] = "List of geometry component dicts."
    v = []
    v.append({"name": "pos", "description": "3-element [x,y,z] position.", "type": "list", "default": "[0,0,0]"})
    v.append({"name": "depth", "description": "Cylinder height in mm.", "type": "number", "default": 250})
    v.append({"name": "radius_name", "description": "Named radius for mode-aware lookup.", "type": "string", "default": '""'})
    v.append({"name": "radius", "description": "Explicit radius in mm.", "type": "number", "default": 0})
    v.append({"name": "radius_rounded", "description": "Rounded edge radius in mm for sphere_cylinder style.", "type": "number", "default": 1})
    v.append({"name": "style", "description": "Output style: sphere_cylinder or cylinder.", "type": "string", "default": '"sphere_cylinder"'})
    v.append({"name": "zz", "description": "Z anchor point: center, bottom, top.", "type": "string", "default": '"center"'})
    v.append({"name": "mode", "description": "Render modes: laser, 3dpr, true.", "type": "list", "default": '["laser","3dpr","true"]'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined = {}
    defined.update(d)
    return defined


def _as_modes(value):
    if isinstance(value, str):
        return [value]
    return list(value)


def _get_depth(kwargs):
    return kwargs.get("depth", kwargs.get("depth_mm", kwargs.get("h", kwargs.get("height", 250))))


def _resolve_depth(depth, mode):
    if isinstance(depth, str):
        import oobb

        return oobb.gv(depth, mode)
    return depth


def _anchored_pos(kwargs, depth):
    pos = copy.deepcopy(kwargs.get("pos", [kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("z", 0)]))
    zz = kwargs.get("zz", "center")
    if isinstance(depth, (int, float)):
        if zz == "center":
            pos[2] -= depth / 2
        elif zz == "top":
            pos[2] -= depth
    return pos


def _resolve_radius(params, mode):
    import oobb

    has_explicit_r = any(key in params for key in ["r", "radius", "d", "diameter", "r1", "r2", "radius_1", "radius_2"])
    radius_name = params.get("radius_name", "")
    if radius_name != "" and not has_explicit_r:
        params["r"] = oobb.gv(radius_name, mode)
        return

    if "radius" in params and "r" not in params:
        params["r"] = params["radius"]
    if "radius_1" in params and "r1" not in params:
        params["r1"] = params["radius_1"]
    if "radius_2" in params and "r2" not in params:
        params["r2"] = params["radius_2"]


def _style_to_shape(style):
    if style in ["cylinder", "plain", "normal"]:
        return "cylinder"
    return "sphere_cylinder"


def action(**kwargs):
    import opsc

    depth = _get_depth(kwargs)
    modes = _as_modes(kwargs.get("mode", ["laser", "3dpr", "true"]))
    style = kwargs.get("style", kwargs.get("cylinder_style", "sphere_cylinder"))

    return_value = []
    for mode in modes:
        depth_for_mode = _resolve_depth(depth, mode)
        params = copy.deepcopy(kwargs)
        params["shape"] = _style_to_shape(style)
        params.setdefault("type", "positive")
        params["h"] = depth_for_mode
        params["pos"] = _anchored_pos(kwargs, depth_for_mode)
        params["inclusion"] = mode
        params.pop("depth", None)
        params.pop("depth_mm", None)
        params.pop("height", None)
        params.pop("style", None)
        params.pop("cylinder_style", None)
        params.pop("mode", None)
        params.pop("zz", None)
        _resolve_radius(params, mode)
        return_value.append(opsc.opsc_easy(**params))

    return return_value


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'depth': 18, 'radius': 7, 'radius_rounded': 2, 'zz': 'center', 'mode': 'true'}},
     {'filename': 'test_2',
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'depth': 18, 'radius': 7, 'radius_rounded': 2, 'style': 'cylinder', 'zz': 'center', 'mode': 'true'}},
     {'filename': 'test_3',
      'preview_rot': [45, 0, 25],
      'kwargs': {'pos': [0, 0, 0], 'depth': 12, 'radius_name': 'hole_radius_m6', 'radius_rounded': 1, 'zz': 'bottom', 'mode': 'true'}}]

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
