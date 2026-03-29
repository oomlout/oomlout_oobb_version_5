d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_tray_lid_thin_spin",
            "name_short": ["tray_lid_thin_spin"],
            "name_long": "OOBB Object: Tray Lid Thin Spin",
            "description": "Auto-generated scaffold for tray_lid_thin_spin. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_tray_lid_thin_spin(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="tray_lid_thin_spin", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
