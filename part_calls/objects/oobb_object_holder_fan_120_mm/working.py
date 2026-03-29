d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_fan_120_mm",
            "name_short": ["holder_fan_120_mm"],
            "name_long": "OOBB Object: Holder Fan 120 Mm",
            "description": "Auto-generated scaffold for holder_fan_120_mm. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_holder_fan_120_mm(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_fan_120_mm", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
