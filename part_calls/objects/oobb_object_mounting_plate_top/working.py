d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_mounting_plate_top",
            "name_short": ["mounting_plate_top"],
            "name_long": "OOBB Object: Mounting Plate Top",
            "description": "Auto-generated scaffold for mounting_plate_top. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_mounting_plate_top(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="mounting_plate_top", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
