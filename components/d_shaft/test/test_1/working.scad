$fn = 50;use <C:\gh\oomlout_oobb_version_5\reference\oomlout_opsc_version_3\cycloid.scad>;

difference() {
	union() {
		difference() {
			translate(v = [0, 0, -8]) {
				cylinder(h = 8, r = 4);
			}
			translate(v = [-4, 2, -8]) {
				cube(size = [8, 2, 8]);
			}
		}
	}
	union();
}
