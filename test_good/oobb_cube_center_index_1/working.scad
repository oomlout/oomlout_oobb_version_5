$fn = 50;


difference() {
	union() {
		translate(v = [-7.5000000000, -7.5000000000, 0]) {
			cube(size = [15, 15, 15]);
		}
	}
	union();
}