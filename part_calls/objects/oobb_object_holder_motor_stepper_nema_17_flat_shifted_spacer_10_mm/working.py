d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm",
            "name_short": ["holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm"],
            "name_long": "OOBB Object: Holder Motor Stepper Nema 17 Flat Shifted Spacer 10 Mm",
            "description": "Auto-generated scaffold for holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm. EDIT THIS.",
            "category": "OOBB Holder",
            "variables": [],
            "source_module": "oobb_get_items_oobb_holder",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_holder

    return oobb_get_items_oobb_holder.get_holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_stepper_nema_17_flat_shifted_spacer_10_mm", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
