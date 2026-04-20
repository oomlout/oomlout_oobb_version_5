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
						translate(v = [0, 0, 2]) {
							hull() {
								translate(v = [-10.0, 5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
								translate(v = [10.0, 5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
								translate(v = [-10.0, -5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
								translate(v = [10.0, -5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
							}
						}
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
						}
						translate(v = [0, 0, 6]) {
							hull() {
								translate(v = [-10.0, 5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
								translate(v = [10.0, 5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
								translate(v = [-10.0, -5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
								translate(v = [10.0, -5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
							}
						}
						translate(v = [13.0, 5.0, 2.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [-13.0, 5.0, 2.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [13.0, 5.0, 6.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [-13.0, 5.0, 6.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [-10.0, 8.0, 2.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, -8.0, 2.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, 8.0, 6.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, -8.0, 6.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, -5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, -5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, 5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, 5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, -5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, -5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, 5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, 5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, -5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
					}
					union();
				}
			}
		}
	}
	union();
}
