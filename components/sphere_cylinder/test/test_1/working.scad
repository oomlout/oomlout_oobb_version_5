$fn = 50;

difference() {
	union() {
		union() {
			cylinder(h = 20, r = 6);
			translate(v = [0, 0, 2]) {
				cylinder(h = 16, r = 8);
			}
			translate(v = [0, 0, 2]) {
				rotate_extrude(angle = 360) {
					translate(v = [6.0, 0, 0]) {
						circle(r = 2.0);
					}
				}
			}
			translate(v = [0, 0, 18]) {
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
