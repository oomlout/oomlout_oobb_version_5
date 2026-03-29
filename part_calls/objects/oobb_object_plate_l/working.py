d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_plate_l",
            "name_short": ["plate_l"],
            "name_long": "OOBB Object: Plate L",
            "description": "Auto-generated scaffold for plate_l. EDIT THIS.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_plate_l(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_l", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
