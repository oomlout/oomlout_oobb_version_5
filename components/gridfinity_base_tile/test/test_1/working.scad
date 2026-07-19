$fn = 50;

use <../scad_reference/gridfinity_base_tile_raw.scad>;

difference() {
	union() {
		translate(v = [0, 0, -6.1]) {
			gridfinity_base_tile_raw(distancex = 0, distancey = 0, fitx = 0, fity = 0);
		}
	}
	union();
}
