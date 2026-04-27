$fn = 50;use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;
use <../../../gridfinity_base_tile/test/test_1/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../gridfinity_base_tile/test/test_2/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_1/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_2/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;

difference() {
	union() {
		linear_extrude(height = 6) {
			polygon(points = [[8.0, 0.0], [4.000000000000001, 6.928203230275509], [-3.9999999999999982, 6.92820323027551], [-8.0, 9.796850830579018e-16], [-4.0000000000000036, -6.928203230275507], [3.9999999999999947, -6.928203230275512]]);
		}
	}
	union();
}
