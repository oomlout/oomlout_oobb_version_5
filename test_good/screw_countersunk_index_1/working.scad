$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -16.0000000000]) {
							cylinder(h = 16, r = 3.0000000000);
						}
						translate(v = [0, 0, -3.7000000000]) {
							cylinder(h = 3.7000000000, r1 = 3.2500000000, r2 = 3.6000000000);
						}
						translate(v = [0, 0, -16.0000000000]) {
							cylinder(h = 16, r = 3.2500000000);
						}
						translate(v = [0, 0, -16.0000000000]) {
							cylinder(h = 16, r = 3.0000000000);
						}
					}
					union();
				}
			}
		}
	}
	union();
}