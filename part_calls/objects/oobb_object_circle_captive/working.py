d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_circle_captive",
            "name_short": ["circle_captive"],
            "name_long": "OOBB Object: Circle Captive",
            "description": "Auto-generated scaffold for circle_captive. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_circle_captive(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="circle_captive", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
