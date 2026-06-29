$fn = 50;

difference() {
	union();
	union() {
		translate(v = [-15.0, -11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, -3.75, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, 3.75, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, 11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-7.5, -11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-7.5, 11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, -11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, 11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [7.5, -11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [7.5, 11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, -11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, -3.75, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, 3.75, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, 11.25, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
	}
}
