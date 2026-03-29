d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder",
            "name_short": ["holder"],
            "name_long": "OOBB Object: Holder",
            "description": "Generates holder-style OOBB geometry for mounting electronic or mechanical components.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "width", "description": "Holder width in OOBB grid units.", "type": "number", "default": 3},
                {"name": "height", "description": "Holder height in OOBB grid units.", "type": "number", "default": 3},
                {"name": "thickness", "description": "Material thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb/oobe).", "type": "string", "default": "oobb"},
            ],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb

    return oobb_get_items_oobb.get_holder(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
