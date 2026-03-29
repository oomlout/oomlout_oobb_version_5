d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bearing_plate_plate",
            "name_short": ["bearing_plate_plate"],
            "name_long": "OOBB Object: Bearing Plate Plate",
            "description": "Auto-generated scaffold for bearing_plate_plate. EDIT THIS.",
            "category": "OOBB Bearing Plate",
            "variables": [{'name': 'thing', 'description': '', 'type': '', 'default': ''}],
            "source_module": "oobb_get_items_oobb_bearing_plate",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_bearing_plate

    return oobb_get_items_oobb_bearing_plate.get_bearing_plate_plate(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing_plate_plate", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
