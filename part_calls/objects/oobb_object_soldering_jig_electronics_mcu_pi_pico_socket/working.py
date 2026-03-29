d = {}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_soldering_jig_electronics_mcu_pi_pico_socket",
            "name_short": ["soldering_jig_electronics_mcu_pi_pico_socket"],
            "name_long": "OOBB Object: Soldering Jig Electronics Mcu Pi Pico Socket",
            "description": "Auto-generated scaffold for soldering_jig_electronics_mcu_pi_pico_socket. EDIT THIS.",
            "category": "OOBB Geometry (Legacy)",
            "variables": [],
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import oobb_get_items_oobb_old

    return oobb_get_items_oobb_old.get_soldering_jig_electronics_mcu_pi_pico_socket(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="soldering_jig_electronics_mcu_pi_pico_socket", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
