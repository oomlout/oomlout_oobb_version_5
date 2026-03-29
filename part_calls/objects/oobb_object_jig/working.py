d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_jig",
            "name_short": ["jig"],
            "name_long": "OOBB Object: Jig",
            "description": "Auto-generated scaffold for jig. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_jig(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="jig", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
