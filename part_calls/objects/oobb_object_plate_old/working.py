d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_plate_old",
            "name_short": ["plate_old"],
            "name_long": "OOBB Object: Plate Old",
            "description": "Auto-generated scaffold for plate_old. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_plate_old(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_old", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
