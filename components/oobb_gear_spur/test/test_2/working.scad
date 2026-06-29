$fn = 50;

include <../scad_reference/oobb_gear_spur_raw.scad>;

difference() {
	union() {
		oobb_gear_spur_raw(backlash = 0, gear_bevel = 1.5, gear_mod = 2, shaft_diam = 6, teeth = 24, thickness = 10);
	}
	union();
}
