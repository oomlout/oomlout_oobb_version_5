d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_wire_higher_voltage",
            "name_short": ["wire_higher_voltage"],
            "name_long": "OOBB Object: Wire Higher Voltage",
            "description": "Auto-generated scaffold for wire_higher_voltage. EDIT THIS.",
            "category": "OOBB Wire",
            "variables": [],
            "source_module": "oobb_get_items_oobb_wire",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_wire_higher_voltage(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire_higher_voltage", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
