d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_tray_vertical",
            "name_short": ["tray_vertical"],
            "name_long": "OOBB Object: Tray Vertical",
            "description": "Auto-generated scaffold for tray_vertical. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_tray_vertical(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="tray_vertical", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
