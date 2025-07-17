$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-4.5000000000, 4.5000000000, 0]) {
								cylinder(h = 5, r = 3);
							}
							translate(v = [4.5000000000, 4.5000000000, 0]) {
								cylinder(h = 5, r = 3);
							}
							translate(v = [-4.5000000000, -4.5000000000, 0]) {
								cylinder(h = 5, r = 3);
							}
							translate(v = [4.5000000000, -4.5000000000, 0]) {
								cylinder(h = 5, r = 3);
							}
						}
					}
					union() {
						hull() {
							translate(v = [-4.5000000000, 4.5000000000, 0]) {
								cylinder(h = 5, r = 1);
							}
							translate(v = [4.5000000000, 4.5000000000, 0]) {
								cylinder(h = 5, r = 1);
							}
							translate(v = [-4.5000000000, -4.5000000000, 0]) {
								cylinder(h = 5, r = 1);
							}
							translate(v = [4.5000000000, -4.5000000000, 0]) {
								cylinder(h = 5, r = 1);
							}
						}
					}
				}
			}
		}
	}
	union();
}