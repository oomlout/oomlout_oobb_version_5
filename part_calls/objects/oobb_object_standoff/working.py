d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_standoff",
            "name_short": ["standoff"],
            "name_long": "OOBB Object: Standoff",
            "description": "Generates a standoff with through-hole for a selected hardware size.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Thread size designation (e.g. m3, m5).", "type": "string", "default": "m3"},
                {"name": "depth", "description": "Standoff length in mm.", "type": "number", "default": 10},
            ],
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_base as ob

    wid = kwargs["radius_name"]
    depth = kwargs["depth"]
    thing = ob.get_default_thing(**kwargs)
    width = ob.gv(f"nut_radius_{wid}_true")

    thing.update({"description": f"standoff {wid}x{depth}x{depth}"})
    thing.update({"width_mm": width})
    thing.update({"depth_mm": depth})
    thing.update({"height_mm": width/1.154})

    th = thing["components"]
    th.extend(ob.oe(t="p", s="oobb_standoff", rn=wid, hole=True, depth=depth))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="standoff", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
