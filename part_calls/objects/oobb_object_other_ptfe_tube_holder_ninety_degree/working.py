d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_other_ptfe_tube_holder_ninety_degree",
            "name_short": ["other_ptfe_tube_holder_ninety_degree"],
            "name_long": "OOBB Object: Other Ptfe Tube Holder Ninety Degree",
            "description": "Auto-generated scaffold for other_ptfe_tube_holder_ninety_degree. EDIT THIS.",
            "category": "OOBB Other",
            "variables": [],
            "source_module": "oobb_get_items_oobb_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_other

    return oobb_get_items_oobb_other.get_other_ptfe_tube_holder_ninety_degree(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="other_ptfe_tube_holder_ninety_degree", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
