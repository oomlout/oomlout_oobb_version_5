$fn = 50;

use <oobb_surface_1559f0ae4a34.scad>;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [65, 0, 25]) {
				difference() {
					union() {
						oobb_surface_1559f0ae4a34();
					}
					union();
				}
			}
		}
	}
	union();
}
