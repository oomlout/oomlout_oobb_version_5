$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [45, 0, 25]) {
				difference() {
					union() {
						translate(v = [0, 0, -2.0]) {
							union() {
								difference() {
									cylinder(h = 4.0, r = 10.0);
									cylinder(h = 4.0, r = 4.0);
								}
								difference() {
									translate(v = [0, 0, -50]) {
										cylinder(h = 100, r = 7.125);
									}
								}
							}
						}
					}
					union();
				}
			}
		}
	}
	union();
}
