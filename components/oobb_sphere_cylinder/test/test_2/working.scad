$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, -9.0]) {
			cylinder(h = 18, r = 7);
		}
	}
	union();
}
