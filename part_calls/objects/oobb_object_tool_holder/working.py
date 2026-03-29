d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_tool_holder",
            "name_short": ["tool_holder"],
            "name_long": "OOBB Object: Tool Holder",
            "description": "Auto-generated scaffold for tool_holder. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_tool_holder(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="tool_holder", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
