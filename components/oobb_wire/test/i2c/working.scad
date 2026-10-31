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
						translate(v = [-2.81, 3.8100000000000005, -1]) {
							cube(size = [8.16, 6.35, 6]);
						}
						translate(v = [-3.81, -12.74, 1.2000000000000002]) {
							cube(size = [10.16, 16.55, 3.8]);
						}
						translate(v = [-8.89, -15.82, 1.2000000000000002]) {
							cube(size = [17.78, 3.08, 3.8]);
						}
						translate(v = [-6.35, -35.82, 1.2000000000000002]) {
							cube(size = [12.7, 20, 3.8]);
						}
						translate(v = [-10.85, -22.0, 1.2000000000000002]) {
							cylinder(h = 3.8, r = 1.5);
						}
					}
				}
			}
		}
	}
	union();
}
