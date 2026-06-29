$fn = 50;

include <../scad_reference/github_belfry_bosl2_gear_raw.scad>;

difference() {
	union() {
		github_belfry_bosl2_gear_raw(backlash = 0, gear_spin = 0, helical = 0, herringbone = false, mod = 2, pressure_angle = 20, shaft_diam = 5, teeth = 16, thickness = 8);
	}
	union();
}
