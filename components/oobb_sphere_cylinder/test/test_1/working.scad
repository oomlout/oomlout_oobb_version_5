$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, -9.0]) {
			union() {
				cylinder(h = 18, r = 5);
				translate(v = [0, 0, 2]) {
					cylinder(h = 14, r = 7);
				}
				translate(v = [0, 0, 2]) {
					rotate_extrude(angle = 360) {
						translate(v = [5.0, 0, 0]) {
							circle(r = 2.0);
						}
					}
				}
				translate(v = [0, 0, 16]) {
					rotate_extrude(angle = 360) {
						translate(v = [5.0, 0, 0]) {
							circle(r = 2.0);
						}
					}
				}
			}
		}
	}
	union();
}
