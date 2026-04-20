$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_1\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_2\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\oobb_cube_hexagon_cutout\test\test_1\oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <C:\gh\oomlout_oobb_version_5\components\oobb_cube_hexagon_cutout\test\test_2\oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [-15.0, -10.0, -5.0]) {
							cube(size = [30, 20, 10]);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
