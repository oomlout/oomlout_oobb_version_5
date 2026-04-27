$fn = 50;use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;
use <../../../gridfinity_base_tile/test/test_1/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../gridfinity_base_tile/test/test_2/gridfinity_base_tile_raw_b06c903fe30da707.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_1/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;
use <../../../oobb_cube_hexagon_cutout/test/test_2/oobb_cube_hexagon_cutout_raw_51d85d3406e2f11c.scad>;

difference() {
	union() {
		difference() {
			linear_extrude(height = 6) {
				polygon(points = [[14.0, 0.0], [9.899494936611665, 9.899494936611664], [8.572244476756641e-16, 14.0], [-9.899494936611664, 9.899494936611665], [-14.0, 1.7144488953513282e-15], [-9.899494936611667, -9.899494936611664], [-2.5716733430269922e-15, -14.0], [9.899494936611664, -9.899494936611667]]);
			}
			linear_extrude(height = 6) {
				polygon(points = [[10.0, 0.0], [7.0710678118654755, 7.071067811865475], [6.123031769111886e-16, 10.0], [-7.071067811865475, 7.0710678118654755], [-10.0, 1.2246063538223773e-15], [-7.071067811865477, -7.071067811865475], [-1.836909530733566e-15, -10.0], [7.071067811865474, -7.071067811865477]]);
			}
		}
	}
	union();
}
