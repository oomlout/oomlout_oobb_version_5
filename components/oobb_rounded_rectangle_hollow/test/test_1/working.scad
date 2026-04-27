$fn = 50;use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;
use <../../../gridfinity_base_tile/test/test_1/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../gridfinity_base_tile/test/test_2/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_1/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_2/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
						}
					}
					union() {
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
						}
					}
				}
			}
		}
	}
	union();
}
