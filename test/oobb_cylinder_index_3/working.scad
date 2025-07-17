$fn = 50;


difference() {
	union() {
		translate(v = [0, 5, -7.5000000000]) {
			cylinder(h = 15, r1 = 6, r2 = 3);
		}
	}
	union();
}