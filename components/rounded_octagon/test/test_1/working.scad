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
		hull() {
			translate(v = [9.228355330395567, 3.8225099362478887, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [3.8225099362478896, 9.228355330395567, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [-3.8225099362478883, 9.228355330395567, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [-9.228355330395567, 3.82250993624789, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [-9.22835533039557, -3.822509936247888, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [-3.822509936247886, -9.22835533039557, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [3.822509936247891, -9.228355330395567, 0]) {
				cylinder(h = 5, r = 3);
			}
			translate(v = [9.22835533039557, -3.8225099362478865, 0]) {
				cylinder(h = 5, r = 3);
			}
		}
	}
	union();
}
