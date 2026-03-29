d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_wire_spacer_long",
            "name_short": ["wire_spacer_long"],
            "name_long": "OOBB Object: Wire Spacer Long",
            "description": "Auto-generated scaffold for wire_spacer_long. EDIT THIS.",
            "category": "OOBB Wire",
            "variables": [],
            "source_module": "oobb_get_items_oobb_wire",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_wire

    return oobb_get_items_oobb_wire.get_wire_spacer_long(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="wire_spacer_long", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
