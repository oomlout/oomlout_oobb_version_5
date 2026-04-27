$fn = 50;use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;
use <../../../gridfinity_base_tile/test/test_1/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../gridfinity_base_tile/test/test_2/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_1/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_2/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;

difference() {
	union();
	union() {
		translate(v = [-15.0, -15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, 0.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, 15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, -15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, 0.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, 15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, -15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, 0.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, 15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
	}
}
