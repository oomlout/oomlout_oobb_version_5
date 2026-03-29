d = {}


def define():
    """Return metadata describing the circle object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_circle",
            "name_short": ["circle"],
            "name_long": "OOBB Object: Circle",
            "description": "Generates circular OOBB plates with optional doughnut, shaft, and bearing features.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "diameter", "description": "Circle diameter in grid units.", "type": "number", "default": 3},
                {"name": "thickness", "description": "Plate thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb or oobe).", "type": "string", "default": "oobb"},
                {"name": "shaft", "description": "Optional shaft type (e.g. coupler_flanged, m3).", "type": "string", "default": ""},
                {"name": "extra", "description": "Extra feature (e.g. doughnut_5).", "type": "string", "default": ""},
                {"name": "both_holes", "description": "Whether to include both oobb and oobe hole patterns.", "type": "boolean", "default": True},
            ],
            "returns": "Thing dict with components list for OpenSCAD generation.",
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the circle thing dict."""
    import copy
    import importlib
    import sys

    import oobb_get_items_oobb

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    thickness = p3.get("thickness", 3)
    zz = p3.get("zz", "bottom")
    pos = p3.get("pos", [0, 0, 0])
    p3.pop("extra", "")
    p3["type"] = f"plate_{extra}"

    if zz == "bottom":
        pos[2] += 0
    elif zz == "middle":
        pos[2] += -thickness / 2
    elif zz == "top":
        pos[2] += -thickness

    if extra != "" and "doughnut" not in extra:
        function_name = "get_plate_" + extra
        importlib.reload(sys.modules[oobb_get_items_oobb.__name__])
        function_to_call = getattr(sys.modules[oobb_get_items_oobb.__name__], function_name)
        return function_to_call(**kwargs)
    else:
        return oobb_get_items_oobb.get_circle_base(**kwargs)


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(diameter=3, thickness=3, size="oobb", type="circle")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
