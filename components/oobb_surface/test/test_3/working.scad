$fn = 50;

use <oobb_surface_ab15fbe710af.scad>;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [65, 0, 25]) {
				difference() {
					union() {
						oobb_surface_ab15fbe710af();
					}
					union();
				}
			}
		}
	}
	union();
}
