d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_test_oobb_screw_countersunk",
            "name_short": ["test_oobb_screw_countersunk"],
            "name_long": "OOBB Object: Test Oobb Screw Countersunk",
            "description": "Wrapper test object for countersunk screw variant cases.",
            "category": "OOBB Test",
            "variables": [
                {"name": "style", "description": "Resolved internally to countersunk.", "type": "string", "default": "countersunk"},
            ],
            "source_module": "oobb_get_items_test",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy
    import oobb_base

    p3 = copy.deepcopy(kwargs)
    p3["style"] = "countersunk"
    p3["type"] = "test_oobb_screw"
    return oobb_base.get_thing_from_dict(p3)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_oobb_screw_countersunk", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
