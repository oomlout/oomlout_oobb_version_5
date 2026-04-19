import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


import importlib.util

def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

d = {}


def describe():
    global d
    d = {}
    d["name"] = 'oobb_screw_countersunk'
    d["name_long"] = 'OOBB Geometry Primitives: Countersunk Screw'
    d["description"] = "Countersunk screw cutout; wrapper over oobb_screw with style='countersunk' pre-set."
    d["category"] = 'Fasteners'
    d["shape_aliases"] = ['screw_countersunk']
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
    """Countersunk screw — delegates to oobb_screw with style pre-set."""
    _screw_mod = _load_component("oobb_screw")
    get_oobb_screw = _screw_mod.action
    kwargs["style"] = "countersunk"
    return get_oobb_screw(**kwargs)

