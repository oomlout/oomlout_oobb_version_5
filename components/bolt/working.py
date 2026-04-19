d = {}


def describe():
    global d
    d = {}
    d["name"] = 'bolt'
    d["name_long"] = 'Fasteners: Bolt'
    d["description"] = 'Generates a hex-head bolt with specified size and length.'
    d["category"] = 'Fasteners'
    d["shape_aliases"] = []
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'radius_name', "description": 'Bolt size designation, e.g. m5, m6.', "type": 'string', "default": '"m6"'})
    v.append({"name": 'depth', "description": 'Bolt length in mm.', "type": 'number', "default": 20})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def action(**kwargs):
    """Build and return the bolt thing dict."""
    import oobb_base as ob

    wid = kwargs["radius_name"]
    depth = kwargs["depth"]
    thing = ob.get_default_thing(**kwargs)
    thing.update({"description": f"bolt {wid}x{depth}"})
    thing.update({"depth_mm": depth})

    thing.update({"components": []})
    thing["components"].extend(ob.oe(
        t="positive", s="oobb_bolt", rn=wid, depth=depth, rotY=0, include_nut=False))

    return thing


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(radius_name="m6", depth=20, type="bolt", size="hardware")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
