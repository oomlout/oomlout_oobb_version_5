d = {}


def define():
    """Return metadata describing the test_gear object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_test_gear",
            "name_short": ["test_gear"],
            "name_long": "OOBB Object: Test Gear",
            "description": "Generates a parametric gear test plate exploring pressure_angle, clearance, and backlash variations.",
            "category": "OOBB Test",
            "variables": [
                {"name": "style", "description": "Gear style variant.", "type": "string", "default": "socket_cap"},
                {"name": "pos", "description": "Position offset [x, y, z].", "type": "array", "default": [0, 0, 0]},
                {"name": "full_object", "description": "Whether to return full thing dict or just components.", "type": "boolean", "default": True},
            ],
            "returns": "Thing dict with test gear components for OpenSCAD generation.",
            "source_module": "oobb_get_items_test",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the test_gear thing dict."""
    import copy
    import oobb_base

    style = kwargs.get("style", "socket_cap")
    kwargs.pop("style", "")
    pos = kwargs.get("pos", [0, 0, 0])
    full_object = kwargs.get("full_object", True)

    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size", "")
    kwargs.pop("extra", "")
    kwargs.pop("type", "")

    pos_current = [0, 0, 0]
    pos_shift = 100
    thickness = 3

    versions = []
    base = {}
    base["shape"] = "gear"
    base["type"] = "p"
    base["shape"] = "gear"
    base["diametral_pitch"] = 0.53333333
    base["number_of_teeth"] = 3 * 8
    base["depth"] = thickness
    base["pos"] = pos_current
    base["comment_extra"] = ""
    base["comment_display"] = True
    base["comment_shift_line"] = 30
    base["extra"] = {}

    versions.append(copy.deepcopy(base))

    tests = {}
    tests["pressure_angle"] = [0, 14.5, 20, 25, 28, 30, 35, 60]
    tests["clearance"] = [0, 0.5, 1, 5]
    tests["backlash"] = [0, 0.5, 1, 2, -1]

    a_extra = "clearance"
    b_extra = "backlash"

    for b in tests[a_extra]:
        for a in tests[b_extra]:
            for v in versions:
                p3 = copy.deepcopy(v)
                comment_extra = v["comment_extra"]
                comment_extra += f" {a_extra} : {a}\n"
                comment_extra += f" {b_extra} : {b}"

                depth = v["depth"]
                p3["comment"] = f"{v['shape']}_{depth}\n{comment_extra}"
                p3["pos"] = copy.deepcopy(pos_current)
                p3[b_extra] = b
                p3[a_extra] = a
                p3["m"] = ""
                extra = v.get("extra", {})
                p3.update(extra)
                oobb_base.append_full(thing, **p3)
                pos_current[1] += pos_shift
        pos_current[0] += pos_shift
        pos_current[1] = 0
    pos_current[0] += pos_shift

    if full_object:
        return thing
    else:
        return thing["components"]


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(type="test", size="oobb", extra="gear")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
