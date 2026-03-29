d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_motor_stepper_nema_17_flat_shifted",
            "name_short": ["holder_motor_stepper_nema_17_flat_shifted"],
            "name_long": "OOBB Object: Holder Motor Stepper Nema 17 Flat Shifted",
            "description": "Auto-generated scaffold for holder_motor_stepper_nema_17_flat_shifted. EDIT THIS.",
            "category": "OOBB Holder",
            "variables": [],
            "source_module": "oobb_get_items_oobb_holder",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_holder

    return oobb_get_items_oobb_holder.get_holder_motor_stepper_nema_17_flat_shifted(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_stepper_nema_17_flat_shifted", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
