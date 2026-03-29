d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_nut_m3",
            "name_short": ["nut_m3"],
            "name_long": "OOBB Object: Nut M3",
            "description": "Auto-generated scaffold for nut_m3. EDIT THIS.",
            "category": "Hardware",
            "variables": [],
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_other

    return oobb_get_items_other.get_nut_m3(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="nut_m3", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
