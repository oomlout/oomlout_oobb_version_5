d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_electronics_potentiometer_17",
            "name_short": ["holder_electronics_potentiometer_17"],
            "name_long": "OOBB Object: Holder Electronics Potentiometer 17",
            "description": "Auto-generated scaffold for holder_electronics_potentiometer_17. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_holder_electronics_potentiometer_17(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_electronics_potentiometer_17", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
