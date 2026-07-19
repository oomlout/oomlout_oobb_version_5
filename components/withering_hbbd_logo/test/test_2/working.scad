$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [55, 0, 25]) {
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										difference() {
											hull() {
												translate(v = [-21.0, -21.0, 0]) {
													cylinder(h = 3.0, r = 4.0);
												}
												translate(v = [21.0, -21.0, 0]) {
													cylinder(h = 3.0, r = 4.0);
												}
												translate(v = [-21.0, 21.0, 0]) {
													cylinder(h = 3.0, r = 4.0);
												}
												translate(v = [21.0, 21.0, 0]) {
													cylinder(h = 3.0, r = 4.0);
												}
											}
											translate(v = [0, 0, 1.5]) {
												linear_extrude(height = 1.51) {
													scale(v = [41.0, 41.0, 1]) {
														translate(v = [-0.5, -0.5, 0]) {
															import(file = "C:/gh/oomlout_oobb_version_5/components/withering_hbbd_logo/image_scad.svg", origin = [0, 0]);
														}
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
			}
		}
	}
	union();
}
