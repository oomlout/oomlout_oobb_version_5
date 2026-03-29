d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_shaft_center",
            "name_short": ["shaft_center"],
            "name_long": "OOBB Object: Shaft Center",
            "description": "Auto-generated scaffold for shaft_center. EDIT THIS.",
            "category": "OOBB Geometry",
            "variables": [{'name': 'thing', 'description': '', 'type': '', 'default': ''}],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_shaft_center(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="shaft_center", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
