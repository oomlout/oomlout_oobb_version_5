$fn = 50;

include <../scad_reference/oobb_gear_spur_raw.scad>;

difference() {
	union() {
		oobb_gear_spur_raw(backlash = 0, gear_bevel = 0, gear_mod = 2, shaft_diam = 5, teeth = 16, thickness = 8);
	}
	union();
}
