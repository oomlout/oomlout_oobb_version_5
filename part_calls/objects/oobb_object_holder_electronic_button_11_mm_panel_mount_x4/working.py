d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_electronic_button_11_mm_panel_mount_x4",
            "name_short": ["holder_electronic_button_11_mm_panel_mount_x4"],
            "name_long": "OOBB Object: Holder Electronic Button 11 Mm Panel Mount X4",
            "description": "Auto-generated scaffold for holder_electronic_button_11_mm_panel_mount_x4. EDIT THIS.",
            "category": "OOBB Holder",
            "variables": [],
            "source_module": "oobb_get_items_oobb_holder",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_holder

    return oobb_get_items_oobb_holder.get_holder_electronic_button_11_mm_panel_mount_x4(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_electronic_button_11_mm_panel_mount_x4", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
