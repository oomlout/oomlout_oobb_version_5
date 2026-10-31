$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [60, 0, 25]) {
				difference() {
					union() {
						intersection() {
							difference() {
								union() {
									translate(v = [0, 0, 0]) {
										rotate(a = [0, 0, 0]) {
											difference() {
												union() {
													translate(v = [0, 0, 2]) {
														hull() {
															translate(v = [-10.0, 5.0, 0]) {
																cylinder(h = 16, r = 5);
															}
															translate(v = [10.0, 5.0, 0]) {
																cylinder(h = 16, r = 5);
															}
															translate(v = [-10.0, -5.0, 0]) {
																cylinder(h = 16, r = 5);
															}
															translate(v = [10.0, -5.0, 0]) {
																cylinder(h = 16, r = 5);
															}
														}
													}
													hull() {
														translate(v = [-10.0, 5.0, 0]) {
															cylinder(h = 2, r = 3);
														}
														translate(v = [10.0, 5.0, 0]) {
															cylinder(h = 2, r = 3);
														}
														translate(v = [-10.0, -5.0, 0]) {
															cylinder(h = 2, r = 3);
														}
														translate(v = [10.0, -5.0, 0]) {
															cylinder(h = 2, r = 3);
														}
													}
													translate(v = [0, 0, 18]) {
														hull() {
															translate(v = [-10.0, 5.0, 0]) {
																cylinder(h = 2, r = 3);
															}
															translate(v = [10.0, 5.0, 0]) {
																cylinder(h = 2, r = 3);
															}
															translate(v = [-10.0, -5.0, 0]) {
																cylinder(h = 2, r = 3);
															}
															translate(v = [10.0, -5.0, 0]) {
																cylinder(h = 2, r = 3);
															}
														}
													}
													translate(v = [13.0, 5.0, 2.0]) {
														rotate(a = [90, 0, 0]) {
															cylinder(h = 10, r = 2);
														}
													}
													translate(v = [-13.0, 5.0, 2.0]) {
														rotate(a = [90, 0, 0]) {
															cylinder(h = 10, r = 2);
														}
													}
													translate(v = [13.0, 5.0, 18.0]) {
														rotate(a = [90, 0, 0]) {
															cylinder(h = 10, r = 2);
														}
													}
													translate(v = [-13.0, 5.0, 18.0]) {
														rotate(a = [90, 0, 0]) {
															cylinder(h = 10, r = 2);
														}
													}
													translate(v = [-10.0, 8.0, 2.0]) {
														rotate(a = [0, 90, 0]) {
															cylinder(h = 20, r = 2);
														}
													}
													translate(v = [-10.0, -8.0, 2.0]) {
														rotate(a = [0, 90, 0]) {
															cylinder(h = 20, r = 2);
														}
													}
													translate(v = [-10.0, 8.0, 18.0]) {
														rotate(a = [0, 90, 0]) {
															cylinder(h = 20, r = 2);
														}
													}
													translate(v = [-10.0, -8.0, 18.0]) {
														rotate(a = [0, 90, 0]) {
															cylinder(h = 20, r = 2);
														}
													}
													translate(v = [-10.0, -5.0, 2]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [10.0, -5.0, 2]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [10.0, 5.0, 2]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [-10.0, 5.0, 2]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [-10.0, -5.0, 18]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [10.0, -5.0, 18]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [10.0, 5.0, 18]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [-10.0, 5.0, 18]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
															}
														}
													}
													translate(v = [-10.0, -5.0, 2]) {
														rotate_extrude(angle = 360) {
															translate(v = [3.0, 0, 0]) {
																circle(r = 2.0);
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
							hull() {
								hull() {
									translate(v = [-11.650898701435649, 6.650898701435649, 0]) {
										cylinder(h = 0.01, r = 3.0);
									}
									translate(v = [11.650898701435649, 6.650898701435649, 0]) {
										cylinder(h = 0.01, r = 3.0);
									}
									translate(v = [-11.650898701435649, -6.650898701435649, 0]) {
										cylinder(h = 0.01, r = 3.0);
									}
									translate(v = [11.650898701435649, -6.650898701435649, 0]) {
										cylinder(h = 0.01, r = 3.0);
									}
								}
								translate(v = [0, 0, 19.99]) {
									hull() {
										translate(v = [-12.0, 7.0, 0]) {
											cylinder(h = 0.01, r = 3.0);
										}
										translate(v = [12.0, 7.0, 0]) {
											cylinder(h = 0.01, r = 3.0);
										}
										translate(v = [-12.0, -7.0, 0]) {
											cylinder(h = 0.01, r = 3.0);
										}
										translate(v = [12.0, -7.0, 0]) {
											cylinder(h = 0.01, r = 3.0);
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
