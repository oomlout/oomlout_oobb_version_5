d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_plate_base",
            "name_short": ["plate_base"],
            "name_long": "OOBB Object: Plate Base",
            "description": "Base rectangular plate geometry with holes and optional extras (gorm, slip_center, slip_end, slip_corner).",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for plate_base."""
    import copy
    import math
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

    th.append(oobb_base.get_comment("plate main", "p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"{size}_plate"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    p3["pos"] = pos
    #p3["m"] = ""
    oobb_base.append_full(thing, **p3)
    #th.append(oobb_base.oobb_easy(**p3))

    # add holes
    if holes:
        th.append(oobb_base.get_comment("holes main", "n"))
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_holes"
        p3["width"] = width
        p3["height"] = height
        p3["pos"] = pos
        p3["both_holes"] = both_holes
        #p3["m"] = ""
        oobb_base.append_full(thing, **p3)
        #th.extend(oobb_base.oobb_easy(**p3))

    ##extra

    if "gorm" in extra:
        th.append(oobb_base.get_comment("extra gorm", "n"))
        holes = [10, 25, 40]
        for h in holes:
            y = (math.floor(height/2) + height % 2) * oobb_base.gv("osp")
            posa = [h, y, 0]
            th.extend(oobb_base.oobb_easy(t="n", s=f"oobb_hole", radius_name="m6", pos=posa, m="#"))
            posa = [-h, 0, 0]
            th.extend(oobb_base.oobb_easy(t="n", s=f"oobb_hole", radius_name="m6", pos=posa, m="#"))
    if "slip_center" in extra:
        th.append(oobb_base.get_comment("extra slip_center", "n"))
        posa = [0, 0, 0]
        th.extend(oobb_base.oobb_easy(t="n", s=f"oobb_hole", radius=9.4/2, pos=posa, m=""))
        posb = [0, 0, thickness/2]
        th.extend(oobb_base.oobb_easy(t="p", s=f"oobb_cylinder", radius=20/2, depth=thickness, pos=posb, m=""))
    if "slip_end" in extra:
        th.append(oobb_base.get_comment("slip_end", "n"))
        posa = [(width-1)/2 * 15, 0, 0]
        th.extend(oobb_base.oobb_easy(t="n", s=f"oobb_hole", radius=9.4/2, pos=posa, m=""))
        posb = [(width-1)/2 * 15, 0, thickness/2]
        th.extend(oobb_base.oobb_easy(t="p", s=f"oobb_cylinder", radius=20/2, depth=thickness, pos=posb, m=""))
    if "slip_corner" in extra:
        th.append(oobb_base.get_comment("slip_corner", "n"))
        posa = [(width-1)/2 * 15, (height-1)/2 * 15, 0]
        th.extend(oobb_base.oobb_easy(t="n", s=f"oobb_hole", radius=9.4/2, pos=posa, m=""))
        posb = [(width-1)/2 * 15, (height-1)/2 * 15, thickness/2]
        th.extend(oobb_base.oobb_easy(t="p", s=f"oobb_cylinder", radius=20/2, depth=thickness, pos=posb, m=""))

    if full_object:
        return thing
    else:  # only return the elements
        return th


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="plate_base", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
