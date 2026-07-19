$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-11.0, 6.0, 0]) {
				cylinder(h = 5, r = 4);
			}
			translate(v = [-11.0, -6.0, 0]) {
				cylinder(h = 5, r = 4);
			}
			translate(v = [11.0, -6.0, 0]) {
				cylinder(h = 5, r = 4);
			}
		}
	}
	union();
}
