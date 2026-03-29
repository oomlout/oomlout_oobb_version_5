d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_nut",
            "name_short": ["nut"],
            "name_long": "OOBB Object: Nut",
            "description": "Generates a hex nut matching the requested hardware thread size.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Thread size designation (e.g. m3, m5).", "type": "string", "default": "m3"},
                {"name": "depth", "description": "Nut thickness/depth in mm.", "type": "number", "default": 3},
            ],
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_base as ob

    wid = kwargs["radius_name"]

    thing = ob.get_default_thing(**kwargs)
    width = ob.gv(f"nut_radius_{wid}_true")
    depth = ob.gv(f"nut_depth_{wid}_true")
    thing.update({"description": f"nut {wid}x{depth}"})
    thing.update({"width_mm": width})
    thing.update({"depth_mm": depth})
    thing.update({"height_mm": width/1.154})

    th = thing["components"]
    th.extend(ob.oe(t="p", s="oobb_nut", rn=wid))
    th.extend(ob.oe(t="n", s="oobb_hole", rn=wid, depth=100, z=-10, m=""))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="nut", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
