d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_trt_old",
            "name_short": ["trt_old"],
            "name_long": "OOBB Object: Trt Old",
            "description": "Auto-generated scaffold for trt_old. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_trt_old(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="trt_old", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
