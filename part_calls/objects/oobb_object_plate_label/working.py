d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_plate_label",
            "name_short": ["plate_label"],
            "name_long": "OOBB Object: Plate Label",
            "description": "Label plate geometry that composes a sub-plate with right-side holes via dispatch.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for plate_label."""
    import copy
    import oobb_base

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)

    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)
    kwargs["pos"] = pos

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "")

    #get the plate
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    shift_x = 0
    shift_y = 0
    shift_z = 0
    pos1 = [pos1[0] + shift_x, pos1[1] + shift_y, pos1[2] + shift_z]
    p3["pos"] = pos1
    p3["type"] = "plate"
    p3["width"] = width
    p3["height"] = height
    p3["holes"] = "right"
    p3["full_object"] = False

    p3.pop("extra", "")
    width_plate = oobb_base.get_thing_from_dict(p3)
    th.append(width_plate)

    if full_object:
        return thing
    else:  # only return the elements
        return th


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_label", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
