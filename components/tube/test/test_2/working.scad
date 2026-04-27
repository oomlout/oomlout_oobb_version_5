$fn = 50;use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;
use <../../../gridfinity_base_tile/test/test_1/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../gridfinity_base_tile/test/test_2/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_1/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_2/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <../../../../pulley_gt2.scad>;
use <../../../raw_scad/test/test_1/main_36cf148840b4395f.scad>;
use <../../../raw_scad/test/test_2/main_6d9aff9ea8473b54.scad>;

difference() {
	union() {
		difference() {
			cylinder(h = 18, r = 13.2);
			cylinder(h = 18, r = 12);
		}
	}
	union();
}
