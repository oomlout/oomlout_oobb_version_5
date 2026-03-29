d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bunting_alphabet",
            "name_short": ["bunting_alphabet"],
            "name_long": "OOBB Object: Bunting Alphabet",
            "description": "Auto-generated scaffold for bunting_alphabet. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_bunting_alphabet(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bunting_alphabet", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
