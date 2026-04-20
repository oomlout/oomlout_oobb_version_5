$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;
use <C:\gh\oomlout_oobb_version_5\components\gridfinity_base_tile\test\test_1\gridfinity_base_tile_raw_b06c903fe30da707.scad>;

difference() {
	union() {
		translate(v = [0, 0, -6.1]) {
			gridfinity_base_tile_raw(distancex = 0, distancey = 0, fitx = 0, fity = 0);
		}
	}
	union();
}
