d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_circle_old_1",
            "name_short": ["circle_old_1"],
            "name_long": "OOBB Object: Circle Old 1",
            "description": "Auto-generated scaffold for circle_old_1. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_circle_old_1(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="circle_old_1", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
