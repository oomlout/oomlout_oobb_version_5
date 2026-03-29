d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_gear_double_stack",
            "name_short": ["gear_double_stack"],
            "name_long": "OOBB Object: Gear Double Stack",
            "description": "Auto-generated scaffold for gear_double_stack. EDIT THIS.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_gear_double_stack(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="gear_double_stack", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
