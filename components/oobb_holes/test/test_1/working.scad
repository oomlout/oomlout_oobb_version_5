$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_1\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_2\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\oobb_cube_hexagon_cutout\test\test_1\oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <C:\gh\oomlout_oobb_version_5\components\oobb_cube_hexagon_cutout\test\test_2\oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;

difference() {
	union();
	union() {
		translate(v = [-15.0, -7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [-15.0, 7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [0.0, -7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [0.0, 7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [15.0, -7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [15.0, 7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
	}
}
