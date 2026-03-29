d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_mounting_plate",
            "name_short": ["mounting_plate"],
            "name_long": "OOBB Object: Mounting Plate",
            "description": "Auto-generated scaffold for mounting_plate. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_mounting_plate(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="mounting_plate", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
