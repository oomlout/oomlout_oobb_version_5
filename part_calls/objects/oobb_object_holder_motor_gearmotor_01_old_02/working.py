d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_holder_motor_gearmotor_01_old_02",
            "name_short": ["holder_motor_gearmotor_01_old_02"],
            "name_long": "OOBB Object: Holder Motor Gearmotor 01 Old 02",
            "description": "Auto-generated scaffold for holder_motor_gearmotor_01_old_02. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_holder_motor_gearmotor_01_old_02(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="holder_motor_gearmotor_01_old_02", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
