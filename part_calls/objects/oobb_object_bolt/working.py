d = {}


def define():
    """Return metadata describing the bolt object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bolt",
            "name_short": ["bolt"],
            "name_long": "OOBB Object: Bolt",
            "description": "Generates a bolt (hex-head fastener) with specified radius and depth.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Bolt size designation (e.g. m5, m6).", "type": "string", "default": "m6"},
                {"name": "depth", "description": "Bolt length in mm.", "type": "number", "default": 20},
            ],
            "returns": "Thing dict with components list for OpenSCAD generation.",
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


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
