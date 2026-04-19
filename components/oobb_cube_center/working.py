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
    d["name"] = 'oobb_cube_center'
    d["name_long"] = 'OOBB Geometry Primitives: Cube Center'
    d["description"] = 'Center-aligned cube that shifts pos by -size/2 on x/y before passing to OpenSCAD.'
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['cube_center']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'size', "description": '[x,y,z] dimensions in mm.', "type": 'list', "default": '(required)'})
    v.append({"name": 'zz', "description": 'Z anchor point: bottom, top, center/middle.', "type": 'string', "default": '"bottom"'})
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
    """Center-aligned cube geometry primitive."""
    p3 = copy.deepcopy(kwargs)
    zz = kwargs.get("zz", "bottom")
    
    p3["shape"] = "cube"
    pos1 = copy.deepcopy(p3["pos"])
    pos1[0] = pos1[0] - p3["size"][0]/2
    pos1[1] = pos1[1] - p3["size"][1]/2
    if zz == "center" or zz == "middle":
        pos1[2] = pos1[2] - p3["size"][2]/2
    elif zz == "top":
        pos1[2] = pos1[2] - p3["size"][2]
    elif zz == "bottom":
        pos1[2] = pos1[2]

    p3["pos"] = pos1
    return oobb.oobb_easy(**p3)
