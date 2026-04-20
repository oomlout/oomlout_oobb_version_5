$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;

difference() {
	union() {
		difference() {
			translate(v = [0, 0, -10]) {
				cylinder(h = 10, r = 6);
			}
			translate(v = [-6, 3, -10]) {
				cube(size = [12, 3, 10]);
			}
		}
	}
	union();
}
