d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_smd_magazine_label_holder",
            "name_short": ["smd_magazine_label_holder"],
            "name_long": "OOBB Object: Smd Magazine Label Holder",
            "description": "Auto-generated scaffold for smd_magazine_label_holder. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_smd_magazine_label_holder(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="smd_magazine_label_holder", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
