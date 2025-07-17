$fn = 50;


difference() {
	union() {
		translate(v = [-5.0000000000, -5.0000000000, 0]) {
			cube(size = [20, 10, 5]);
		}
	}
	union();
}