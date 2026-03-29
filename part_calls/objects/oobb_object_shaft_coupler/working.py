d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_shaft_coupler",
            "name_short": ["shaft_coupler"],
            "name_long": "OOBB Object: Shaft Coupler",
            "description": "Auto-generated scaffold for shaft_coupler. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_shaft_coupler(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="shaft_coupler", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
