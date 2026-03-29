d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_wire_basic_basic_basic",
            "name_short": ["wire_basic_basic_basic"],
            "name_long": "OOBB Object: Wire Basic Basic Basic",
            "description": "Auto-generated scaffold for wire_basic_basic_basic. EDIT THIS.",
            "category": "OOBB Wire",
            "variables": [],
            "source_module": "oobb_get_items_oobb_wire",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_wire_basic_basic_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire_basic_basic_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
