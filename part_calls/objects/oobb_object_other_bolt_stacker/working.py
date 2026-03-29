d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_other_bolt_stacker",
            "name_short": ["other_bolt_stacker"],
            "name_long": "OOBB Object: Other Bolt Stacker",
            "description": "Auto-generated scaffold for other_bolt_stacker. EDIT THIS.",
            "category": "OOBB Other",
            "variables": [],
            "source_module": "oobb_get_items_oobb_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_other

    return oobb_get_items_oobb_other.get_other_bolt_stacker(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="other_bolt_stacker", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
