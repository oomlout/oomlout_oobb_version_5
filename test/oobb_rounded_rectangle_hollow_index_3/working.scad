$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 5, r2 = 3);
							}
							translate(v = [5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 5, r2 = 3);
							}
							translate(v = [-5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 5, r2 = 3);
							}
							translate(v = [5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 5, r2 = 3);
							}
						}
					}
					union() {
						hull() {
							translate(v = [-4.0000000000, -1.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 4, r2 = 2);
							}
							translate(v = [4.0000000000, -1.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 4, r2 = 2);
							}
							translate(v = [-4.0000000000, 1.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 4, r2 = 2);
							}
							translate(v = [4.0000000000, 1.0000000000, 0]) {
								cylinder(h = 5, r = 5, r1 = 4, r2 = 2);
							}
						}
					}
				}
			}
		}
	}
	union();
}