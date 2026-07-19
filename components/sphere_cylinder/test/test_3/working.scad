$fn = 50;

difference() {
	union() {
		union() {
			translate(v = [0, 0, -10.0]) {
				cylinder(h = 20, r = 6);
			}
			translate(v = [0, 0, -8.0]) {
				cylinder(h = 16, r = 8);
			}
			translate(v = [0, 0, -8.0]) {
				rotate_extrude(angle = 360) {
					translate(v = [6.0, 0, 0]) {
						circle(r = 2.0);
					}
				}
			}
			translate(v = [0, 0, 8.0]) {
				rotate_extrude(angle = 360) {
					translate(v = [6.0, 0, 0]) {
						circle(r = 2.0);
					}
				}
			}
		}
	}
	union();
}
