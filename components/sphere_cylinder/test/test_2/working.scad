$fn = 50;

difference() {
	union() {
		union() {
			cylinder(h = 12, r = 6.0);
			translate(v = [0, 0, 3]) {
				cylinder(h = 6, r = 9.0);
			}
			translate(v = [0, 0, 3]) {
				rotate_extrude(angle = 360) {
					translate(v = [6.0, 0, 0]) {
						circle(r = 3.0);
					}
				}
			}
			translate(v = [0, 0, 9]) {
				rotate_extrude(angle = 360) {
					translate(v = [6.0, 0, 0]) {
						circle(r = 3.0);
					}
				}
			}
		}
	}
	union();
}
