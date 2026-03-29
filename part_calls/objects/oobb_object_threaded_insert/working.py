d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_threaded_insert",
            "name_short": ["threaded_insert"],
            "name_long": "OOBB Object: Threaded Insert",
            "description": "Generates a heat-set threaded insert profile plus pilot hole geometry.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Thread size designation (e.g. m3, m4).", "type": "string", "default": "m3"},
                {"name": "style", "description": "Insert style profile identifier.", "type": "string", "default": "01"},
            ],
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_base as ob

    wid = kwargs["radius_name"]
    style = kwargs.get("style", "01")
    thing = ob.get_default_thing(**kwargs)
    width = ob.gv(f"threaded_insert_{style}_radius_{wid}_true")
    depth = ob.gv(f"threaded_insert_{style}_depth_{wid}_true")
    thing.update({"description": f"threaded insert {wid}x{depth}"})
    thing.update({"width_mm": width})
    thing.update({"depth_mm": depth})

    th = thing["components"]
    th.extend(ob.oe(t="p", s="oobb_threaded_insert", rn=wid, hole=False))
    th.extend(ob.oe(t="n", s="oobb_hole", rn=wid, depth=100, z=-10, m=""))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="threaded_insert", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
