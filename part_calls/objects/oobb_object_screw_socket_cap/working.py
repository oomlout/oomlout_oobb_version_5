d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_screw_socket_cap",
            "name_short": ["screw_socket_cap"],
            "name_long": "OOBB Object: Screw Socket Cap",
            "description": "Generates a socket head cap screw with configurable thread size and length.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Screw thread size (e.g. m3, m5).", "type": "string", "default": "m3"},
                {"name": "depth", "description": "Screw length/depth in mm.", "type": "number", "default": 12},
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
    thing.update({"description": f"screw socket cap {wid}x{depth}"})
    thing.update({"depth_mm": depth})

    thing.update({"components": []})
    thing["components"].extend(ob.oe(
        t="positive", s="oobb_screw_socket_cap", rn=wid, depth=depth, include_nut=False))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="screw_socket_cap", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
