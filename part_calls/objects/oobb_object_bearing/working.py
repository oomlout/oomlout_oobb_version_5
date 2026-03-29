d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bearing",
            "name_short": ["bearing"],
            "name_long": "OOBB Object: Bearing",
            "description": "Generates a bearing model (for example 606/608 series) for rotational assemblies.",
            "category": "Hardware",
            "variables": [
                {"name": "bearing_name", "description": "Bearing designation (e.g. 606, 608).", "type": "string", "default": "608"},
                {"name": "exclude_clearance", "description": "Exclude outer clearance geometry if true.", "type": "boolean", "default": False},
            ],
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_base as ob

    bearing_name = kwargs["bearing_name"]
    thing = ob.get_default_thing(**kwargs)
    thing.update({"description": f"bearing {bearing_name}"})

    th = thing["components"]
    th.extend(ob.oe(t="positive", s="oobb_cylinder",
              radius_name=f'bearing_{bearing_name}_od', depth=f"bearing_{bearing_name}_depth"))
    th.extend(ob.oe(t="negative", s="oobb_cylinder",
              radius_name=f'bearing_{bearing_name}_id', depth=f"bearing_{bearing_name}_depth"))

    return thing


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="bearing", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
