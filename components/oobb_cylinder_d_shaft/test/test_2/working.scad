$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -6.0]) {
							cylinder(h = 12, r = 5);
						}
					}
					union() {
						translate(v = [-5.1, 4, -6.1]) {
							cube(size = [10.2, 1.1, 12.2]);
						}
					}
				}
			}
		}
	}
	union();
}
