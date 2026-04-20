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
		linear_extrude(height = 3) {
			text(font = "DejaVu Sans:style=Bold", halign = "center", size = 10, text = "OOBB", valign = "center");
		}
	}
	union();
}
