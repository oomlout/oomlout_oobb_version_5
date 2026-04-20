import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# ---------- cross-component helper imports ----------
import importlib.util
def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_screw_mod = _load_component("oobb_screw")
get_oobb_screw = _screw_mod.action

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_screw_socket_cap'
    d["name_long"] = 'OOBB Geometry Primitives: Socket Cap Screw'
    d["description"] = "Socket-cap screw cutout; wrapper over oobb_screw with style='socket_cap' pre-set."
    d["category"] = 'Fasteners'
    d["shape_aliases"] = ['screw_socket_cap']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: p/positive or n/negative.', "type": 'string', "default": 'p'})
    v.append({"name": 'radius_name', "description": 'Named radius key, e.g. m3, m6.', "type": 'string', "default": '"m3"'})
    v.append({"name": 'depth', "description": 'Shaft hole depth in mm.', "type": 'number', "default": 250})
    v.append({"name": 'zz', "description": 'Z anchor: none, top, bottom.', "type": 'string', "default": '"none"'})
    v.append({"name": 'hole', "description": 'Include a through shaft hole.', "type": 'bool', "default": True})
    v.append({"name": 'mode', "description": 'Render modes: laser, 3dpr, true.', "type": 'list', "default": '["laser","3dpr","true"]'})
    v.append({"name": 'rot', "description": 'Rotation [rx,ry,rz] in degrees.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'rot_x', "description": 'X rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_y', "description": 'Y rotation in degrees.', "type": 'number', "default": 0})
    v.append({"name": 'rot_z', "description": 'Z rotation in degrees.', "type": 'number', "default": 0})
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
    """Socket cap screw â€” delegates to oobb_screw with style pre-set."""
    import importlib.util, os
    def _load_component(folder_name):
        path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
        spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    get_oobb_screw = _load_component("oobb_screw").action
    kwargs["style"] = "socket_cap"
    return get_oobb_screw(**kwargs)


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [70, 0, 20],
      'kwargs': {'pos': [0, 0, 0],
                 'type': 'positive',
                 'radius_name': 'm3',
                 'depth': 16,
                 'zz': 'none',
                 'hole': True,
                 'mode': 'true',
                 'rot': [0, 0, 0]}}]

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


