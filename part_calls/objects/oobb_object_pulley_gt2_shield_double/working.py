d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_pulley_gt2_shield_double",
            "name_short": ["pulley_gt2_shield_double"],
            "name_long": "OOBB Object: Pulley Gt2 Shield Double",
            "description": "Auto-generated scaffold for pulley_gt2_shield_double. EDIT THIS.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_pulley_gt2_shield_double(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="pulley_gt2_shield_double", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
