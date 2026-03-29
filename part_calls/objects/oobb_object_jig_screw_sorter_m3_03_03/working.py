d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_jig_screw_sorter_m3_03_03",
            "name_short": ["jig_screw_sorter_m3_03_03"],
            "name_long": "OOBB Object: Jig Screw Sorter M3 03 03",
            "description": "Auto-generated scaffold for jig_screw_sorter_m3_03_03. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_jig_screw_sorter_m3_03_03(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="jig_screw_sorter_m3_03_03", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
