$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_1\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_2\gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <C:\gh\oomlout_oobb_version_5\components\oobb_cube_hexagon_cutout\test\test_1\oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <C:\gh\oomlout_oobb_version_5\components\oobb_cube_hexagon_cutout\test\test_2\oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <C:\gh\oomlout_oobb_version_5\pulley_gt2.scad>;
use <C:\gh\oomlout_oobb_version_5\components\raw_scad\test\test_1\main_36cf148840b4395f.scad>;
use <C:\gh\oomlout_oobb_version_5\components\raw_scad\test\test_2\main_6d9aff9ea8473b54.scad>;

difference() {
	union() {
		difference() {
			hull() {
				translate(v = [-11.0, 6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
				translate(v = [11.0, 6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
				translate(v = [-11.0, -6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
				translate(v = [11.0, -6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
			}
			translate(v = [0, 0, 0.6]) {
				hull() {
					union() {
						translate(v = [-10.0, 5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [-10.0, 5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [-10.0, 5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
					union() {
						translate(v = [10.0, 5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [10.0, 5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [10.0, 5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
					union() {
						translate(v = [-10.0, -5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [-10.0, -5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [-10.0, -5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
					union() {
						translate(v = [10.0, -5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [10.0, -5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [10.0, -5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
				}
			}
		}
	}
	union();
}
