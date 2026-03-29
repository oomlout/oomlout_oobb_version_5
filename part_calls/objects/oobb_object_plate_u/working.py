d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_plate_u",
            "name_short": ["plate_u"],
            "name_long": "OOBB Object: Plate U",
            "description": "Auto-generated scaffold for plate_u. EDIT THIS.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_plate_u(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_u", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
