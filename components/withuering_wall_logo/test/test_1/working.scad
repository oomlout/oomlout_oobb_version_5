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
											cylinder(h = 3.0, r = 20.0);
											translate(v = [0, 0, -0.01]) {
												linear_extrude(height = 3.02) {
													scale(v = [28.0, 28.0, 1]) {
														translate(v = [-0.5, 0, 0]) {
															import(file = "withuering_wall_logo.svg", origin = [0, 0]);
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
