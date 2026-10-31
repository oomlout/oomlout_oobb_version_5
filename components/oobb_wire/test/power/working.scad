$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-17.0, 17.0, 0]) {
								cylinder(h = 4, r = 5);
							}
							translate(v = [17.0, 17.0, 0]) {
								cylinder(h = 4, r = 5);
							}
							translate(v = [-17.0, -17.0, 0]) {
								cylinder(h = 4, r = 5);
							}
							translate(v = [17.0, -17.0, 0]) {
								cylinder(h = 4, r = 5);
							}
						}
					}
					union() {
						translate(v = [-1.54, -3.8099999999999996, -1]) {
							cube(size = [3.08, 6.35, 6]);
						}
						translate(v = [-2.54, -12.74, 1.2000000000000002]) {
							cube(size = [5.08, 14.0, 3.8]);
						}
						translate(v = [-7.619999999999999, -15.82, 1.2000000000000002]) {
							cube(size = [12.7, 3.08, 3.8]);
						}
						translate(v = [-5.08, -35.82, 1.2000000000000002]) {
							cube(size = [7.62, 20, 3.8]);
						}
						translate(v = [-9.58, -22.0, 1.2000000000000002]) {
							cylinder(h = 3.8, r = 1.5);
						}
					}
				}
			}
		}
	}
	union();
}
