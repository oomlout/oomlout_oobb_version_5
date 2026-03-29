d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_test_hole",
            "name_short": ["test_hole"],
            "name_long": "OOBB Object: Test Hole",
            "description": "Generates a plate with a grid of progressively sized hole cutouts for fit testing.",
            "category": "OOBB Test",
            "variables": [
                {"name": "width", "description": "Plate width in grid units.", "type": "number", "default": 3},
                {"name": "height", "description": "Plate height in grid units.", "type": "number", "default": 3},
                {"name": "shaft", "description": "Starting hole diameter in mm.", "type": "number", "default": 3},
                {"name": "bearing", "description": "Increment step between holes in mm.", "type": "number", "default": 0.5},
                {"name": "thickness", "description": "Plate thickness in mm.", "type": "number", "default": 3},
            ],
            "source_module": "oobb_get_items_test",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import copy
    import math
    import oobb_base

    kwargs.pop("style", "")
    pos = kwargs.get("pos", [0, 0, 0])
    full_object = kwargs.get("full_object", True)
    hole_size = kwargs.get("shaft", 3)
    increment = kwargs.get("bearing", 0.5)

    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")
    kwargs.pop("type", "")
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    thickness = kwargs.get("thickness", 3)

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "oobb_plate"
    p3["type"] = "positive"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    oobb_base.append_full(thing, **p3)

    wid = width
    hei = height
    extra = -increment * 4
    for w in range(0, wid):
        for h in range(0, hei):
            p3 = copy.deepcopy(kwargs)
            p3["shape"] = "oobb_hole"
            p3["type"] = "negative"
            p3["width"] = wid
            p3["height"] = hei
            p3["depth"] = 3
            x = (w * 15) - math.floor(wid / 2) * 15
            y = (h * 15) - math.floor(hei / 2) * 15
            pos1 = copy.deepcopy(p3["pos"])
            pos1[0] += x
            pos1[1] += y
            p3["pos"] = pos1
            p3["radius"] = (hole_size + extra) / 2
            oobb_base.append_full(thing, **p3)
            extra += increment

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="test_hole", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
