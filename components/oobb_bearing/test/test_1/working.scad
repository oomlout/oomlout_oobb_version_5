$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [45, 0, 25]) {
				difference() {
					union() {
						translate(v = [0, 0, -3.0]) {
							union() {
								difference() {
									cylinder(h = 6.0, r = 17.0);
									cylinder(h = 6.0, r = 6.0);
								}
								difference() {
									translate(v = [0, 0, -50]) {
										cylinder(h = 100, r = 11.5);
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
