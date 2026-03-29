d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_other_corner_cube_relief",
            "name_short": ["other_corner_cube_relief"],
            "name_long": "OOBB Object: Other Corner Cube Relief",
            "description": "Auto-generated scaffold for other_corner_cube_relief. EDIT THIS.",
            "category": "OOBB Other",
            "variables": [],
            "source_module": "oobb_get_items_oobb_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_other

    return oobb_get_items_oobb_other.get_other_corner_cube_relief(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="other_corner_cube_relief", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
