d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_wheel",
            "name_short": ["wheel"],
            "name_long": "OOBB Object: Wheel",
            "description": "Auto-generated scaffold for wheel. EDIT THIS.",
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
    p3.pop("extra", "")
    p3["type"] = f"wheel_{extra}"

    if type(extra) == list:
        extra = "_".join(extra)
    current_module = __import__("oobb_get_items_oobb_wheel")
    if extra != "":
        function_name = "get_wheel_" + extra
    else:
        function_name = "get_wheel"
    function_to_call = getattr(current_module, function_name)
    return function_to_call(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wheel", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
