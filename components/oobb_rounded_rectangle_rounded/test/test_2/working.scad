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
						translate(v = [0, 0, 3]) {
							hull() {
								translate(v = [-12.0, 6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
								translate(v = [12.0, 6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
								translate(v = [-12.0, -6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
								translate(v = [12.0, -6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
							}
						}
						hull() {
							translate(v = [-12.0, 6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
							translate(v = [12.0, 6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
							translate(v = [-12.0, -6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
							translate(v = [12.0, -6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
						}
						translate(v = [0, 0, 7]) {
							hull() {
								translate(v = [-12.0, 6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
								translate(v = [12.0, 6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
								translate(v = [-12.0, -6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
								translate(v = [12.0, -6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
							}
						}
						translate(v = [15.0, 6.0, 3.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [-15.0, 6.0, 3.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [15.0, 6.0, 7.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [-15.0, 6.0, 7.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [-12.0, 9.0, 3.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, -9.0, 3.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, 9.0, 7.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, -9.0, 7.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, -6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, -6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, 6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, 6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, -6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, -6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, 6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, 6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, -6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
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
