d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_ci_holes_center",
            "name_short": ["ci_holes_center"],
            "name_long": "OOBB Object: Ci Holes Center",
            "description": "Auto-generated scaffold for ci_holes_center. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [{'name': 'thing', 'description': '', 'type': '', 'default': ''}],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_ci_holes_center(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="ci_holes_center", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
