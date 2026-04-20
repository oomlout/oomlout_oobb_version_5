$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_1\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_2\gridfinity_base_tile_raw_b06c903fe30da707.scad>;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [5.657, 5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [-5.657, -5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [5.657, -5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [-5.657, 5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [0, 0, -100.0]) {
							cylinder(h = 200, r = 4.0);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
