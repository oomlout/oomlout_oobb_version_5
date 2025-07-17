$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, -1.5000000000]) {
			hull() {
				translate(v = [-26.0000000000, 24.5000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
				translate(v = [26.0000000000, 24.5000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
				translate(v = [-26.0000000000, -24.5000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
				translate(v = [26.0000000000, -24.5000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
			}
		}
	}
	union() {
		translate(v = [-22.5000000000, -22.5000000000, 0]) {
			cylinder(h = 100, r = 3.2500000000);
		}
		translate(v = [-22.5000000000, -7.5000000000, 0]) {
			cylinder(h = 100, r = 3.2500000000);
		}
		translate(v = [-22.5000000000, 7.5000000000, 0]) {
			cylinder(h = 100, r = 3.2500000000);
		}
		translate(v = [0, 30, -100.0000000000]) {
			cylinder(h = 200, r = 4.8500000000);
		}
	}
}