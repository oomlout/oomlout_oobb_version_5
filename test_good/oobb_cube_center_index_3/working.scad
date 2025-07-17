$fn = 50;


difference() {
	union() {
		translate(v = [-10.0000000000, -7.5000000000, 0]) {
			cube(size = [10, 5, 10]);
		}
	}
	union();
}