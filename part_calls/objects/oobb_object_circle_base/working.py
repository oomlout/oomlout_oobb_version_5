d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_circle_base",
            "name_short": ["circle_base"],
            "name_long": "OOBB Object: Circle Base",
            "description": "Base circular geometry builder with optional shaft, holes, and doughnut cutout.",
            "category": "OOBB Geometry",
            "variables": [],
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for circle_base."""
    import copy
    import oobb_base
    from oobb_arch.helpers.shaft_helpers import get_shaft_center

    # default sets
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    diameter = kwargs.get("diameter", 1)
    width = diameter
    height = diameter
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    shaft = kwargs.get("shaft", "")

    # extra sets
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)
    kwargs["pos"] = pos

    # get the default thing
    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "")

    th.append(oobb_base.get_comment("circle main", "p"))
    # add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"{size}_circle"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = thickness
    p3["pos"] = pos
    #p3["m"] = ""
    oobb_base.append_full(thing, **p3)

    doughnut_diameter = 0
    #doughnut_cutout
    if "doughnut" in extra:
        doughnut_diameter = float(extra.replace("doughnut_", ""))
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_circle"
        p3["width"] = doughnut_diameter
        p3["height"] = doughnut_diameter
        p3["depth"] = thickness
        p3["pos"] = pos
        p3["diameter"] = doughnut_diameter
        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)

    # add holes
    if holes:
        th.append(oobb_base.get_comment("holes main", "n"))
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"{size}_holes"
        p3["width"] = width
        p3["height"] = height
        p3["pos"] = pos
        p3["holes"] = "all"
        p3["both_holes"] = both_holes
        p3["circle"] = True
        if shaft != "":
            p3["middle"] = False
            pass

        #p3["m"] = "#"
        oobb_base.append_full(thing, **p3)
        #th.extend(oobb_base.oobb_easy(**p3))

        if diameter == 1.5:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = f"{size}_hole"
            p3["width"] = width
            p3["height"] = height
            p3["pos"] = pos
            p3["radius_name"] = "m3"
            poss = []
            shift = 5.303
            poss.append([shift, shift, 0])
            poss.append([-shift, shift, 0])
            poss.append([shift, -shift, 0])
            poss.append([-shift, -shift, 0])
            p3["pos"] = poss
            p3["m"] = "#"
            oobb_base.append_full(thing, **p3)

    if shaft != "":
        get_shaft_center(thing, **kwargs)

    if full_object:
        return thing
    else:  # only return the elements
        return th


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="circle_base", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
