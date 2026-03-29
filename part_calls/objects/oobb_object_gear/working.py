d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_gear",
            "name_short": ["gear"],
            "name_long": "OOBB Object: Gear",
            "description": "Generates parametric OOBB-compatible gears for rotational assemblies.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "teeth", "description": "Number of gear teeth.", "type": "number", "default": 20},
                {"name": "thickness", "description": "Gear thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb/oobe).", "type": "string", "default": "oobb"},
            ],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_gear(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="gear", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
