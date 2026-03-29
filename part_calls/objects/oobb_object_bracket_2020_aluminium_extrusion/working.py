d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bracket_2020_aluminium_extrusion",
            "name_short": ["bracket_2020_aluminium_extrusion"],
            "name_long": "OOBB Object: Bracket 2020 Aluminium Extrusion",
            "description": "Auto-generated scaffold for bracket_2020_aluminium_extrusion. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_bracket_2020_aluminium_extrusion(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bracket_2020_aluminium_extrusion", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
