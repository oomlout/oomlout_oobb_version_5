d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_oobb_wire_base",
            "name_short": ["oobb_wire_base"],
            "name_long": "OOBB Object: Oobb Wire Base",
            "description": "Auto-generated scaffold for oobb_wire_base. EDIT THIS.",
            "category": "OOBB Wire",
            "variables": [],
            "source_module": "oobb_get_items_oobb_wire",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_oobb_wire_base(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="oobb_wire_base", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
