$fn = 50;

difference() {
	union() {
		union() {
			cylinder(h = 12, r = 2.0);
			translate(v = [0, 0, 1]) {
				cylinder(h = 10, r = 3.0);
			}
			translate(v = [0, 0, 1]) {
				rotate_extrude(angle = 360) {
					translate(v = [2.0, 0, 0]) {
						circle(r = 1.0);
					}
				}
			}
			translate(v = [0, 0, 11]) {
				rotate_extrude(angle = 360) {
					translate(v = [2.0, 0, 0]) {
						circle(r = 1.0);
					}
				}
			}
		}
	}
	union();
}
