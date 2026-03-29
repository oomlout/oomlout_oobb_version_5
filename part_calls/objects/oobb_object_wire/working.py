d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_wire",
            "name_short": ["wire"],
            "name_long": "OOBB Object: Wire",
            "description": "Auto-generated scaffold for wire. EDIT THIS.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra")
    p3["type"] = f"wire_{extra}"
    if extra != "":
        if type(extra) == list:
            extra = "_".join(extra)
        current_module = __import__("oobb_get_items_oobb_wire")
        function_name = "get_wire_" + extra
        try:
            function_to_call = getattr(current_module, function_name)
        except:
            function_to_call = getattr(current_module, "get_oobb_wire_base")
        return function_to_call(**kwargs)
    else:
        raise Exception("No extra")


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
