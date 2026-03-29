d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_motor_servo_standard_01_top",
            "name_short": ["holder_motor_servo_standard_01_top"],
            "name_long": "OOBB Object: Holder Motor Servo Standard 01 Top",
            "description": "Auto-generated scaffold for holder_motor_servo_standard_01_top. EDIT THIS.",
            "category": "OOBB Holder",
            "variables": [],
            "source_module": "oobb_get_items_oobb_holder",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_holder

    return oobb_get_items_oobb_holder.get_holder_motor_servo_standard_01_top(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_servo_standard_01_top", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
