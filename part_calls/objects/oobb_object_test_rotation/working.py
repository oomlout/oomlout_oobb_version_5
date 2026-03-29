d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_test_rotation",
            "name_short": ["test_rotation"],
            "name_long": "OOBB Object: Test Rotation",
            "description": "Generates rotation/transform debug fixtures for item orientation verification.",
            "category": "OOBB Test",
            "variables": [
                {"name": "thickness", "description": "Fixture thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb/oobe).", "type": "string", "default": "oobb"},
                {"name": "holes", "description": "Include reference holes.", "type": "boolean", "default": True},
            ],
            "source_module": "oobb_get_items_test",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy
    import oobb_base

    thickness = kwargs.get("thickness", 3)
    kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)

    kwargs.get("holes", True)
    kwargs.get("both_holes", False)
    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")

    pos_current = [0, 0, 0]
    comment_extra = ""

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    pos_current = [300, 0, 0]
    comment_extra = " rot_y : 180"

    item = "oobb_screw_socket_cap_shape_m3_radius_name_12_mm_depth"
    p3 = copy.deepcopy(kwargs)
    p3["comment"] = f"{item}{comment_extra}\n"
    p3["pos"] = copy.deepcopy(pos_current)
    p3["item"] = item
    p3["rot_y"] = 180
    p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_rotation", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
