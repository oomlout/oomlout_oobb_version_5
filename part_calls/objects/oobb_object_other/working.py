d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_other",
            "name_short": ["other"],
            "name_long": "OOBB Object: Other",
            "description": "Auto-generated scaffold for other. EDIT THIS.",
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
    p3["type"] = f"holder_{extra}"
    if extra != "":
        current_module = __import__("oobb_get_items_oobb_other")
        function_name = "get_other_" + extra
        function_to_call = getattr(current_module, function_name)
        return function_to_call(**kwargs)
    else:
        raise Exception("No extra")


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="other", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
