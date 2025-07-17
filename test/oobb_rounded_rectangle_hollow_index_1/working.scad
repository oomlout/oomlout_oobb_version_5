$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
							translate(v = [5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
							translate(v = [-5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
							translate(v = [5.0000000000, 0.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
						}
					}
					union() {
						hull() {
							translate(v = [-3.0000000000, -2.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
							translate(v = [3.0000000000, -2.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
							translate(v = [-3.0000000000, 2.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
							translate(v = [3.0000000000, 2.0000000000, 0]) {
								cylinder(h = 5, r = 5);
							}
						}
					}
				}
			}
		}
	}
	union();
}