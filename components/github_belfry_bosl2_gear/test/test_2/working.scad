$fn = 50;

include <../scad_reference/github_belfry_bosl2_gear_raw.scad>;

difference() {
	union() {
		github_belfry_bosl2_gear_raw(backlash = 0, gear_spin = 0, helical = 20, herringbone = true, mod = 2, pressure_angle = 20, shaft_diam = 6, teeth = 24, thickness = 10);
	}
	union();
}
