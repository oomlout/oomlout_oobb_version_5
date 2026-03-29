d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_jack_basic",
            "name_short": ["jack_basic"],
            "name_long": "OOBB Object: Jack Basic",
            "description": "Auto-generated scaffold for jack_basic. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_jack_basic(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="jack_basic", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
