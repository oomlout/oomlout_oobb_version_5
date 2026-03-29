d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_tool_holder_tool_holder_basic",
            "name_short": ["tool_holder_tool_holder_basic"],
            "name_long": "OOBB Object: Tool Holder Tool Holder Basic",
            "description": "Auto-generated scaffold for tool_holder_tool_holder_basic. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_tool_holder_tool_holder_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="tool_holder_tool_holder_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
