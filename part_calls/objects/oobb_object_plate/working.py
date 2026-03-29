d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_plate",
            "name_short": ["plate"],
            "name_long": "OOBB Object: Plate",
            "description": "Generates rectangular OOBB plates with configurable width, height, and hole patterns.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "width", "description": "Plate width in OOBB grid units.", "type": "number", "default": 3},
                {"name": "height", "description": "Plate height in OOBB grid units.", "type": "number", "default": 3},
                {"name": "thickness", "description": "Plate thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb/oobe).", "type": "string", "default": "oobb"},
            ],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy
    import importlib
    import sys

    import oobb_get_items_oobb

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra", "")
    p3["type"] = f"plate_{extra}"
    if extra != "":
        function_name = "get_plate_" + extra
        importlib.reload(sys.modules[oobb_get_items_oobb.__name__])
        try:
            function_to_call = getattr(sys.modules[oobb_get_items_oobb.__name__], function_name)
            return function_to_call(**kwargs)
        except Exception:
            print(f"Function {function_name} not found using basic plate")
            return oobb_get_items_oobb.get_plate_base(**kwargs)
    else:
        return oobb_get_items_oobb.get_plate_base(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
