$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0.4]) {
							hull() {
								translate(v = [-12.0, 6.0, 0]) {
									cylinder(h = 9.2, r = 6);
								}
								translate(v = [12.0, 6.0, 0]) {
									cylinder(h = 9.2, r = 6);
								}
								translate(v = [-12.0, -6.0, 0]) {
									cylinder(h = 9.2, r = 6);
								}
								translate(v = [12.0, -6.0, 0]) {
									cylinder(h = 9.2, r = 6);
								}
							}
						}
						hull() {
							translate(v = [-12.000000000000002, 6.0, 0]) {
								cylinder(h = 0.4, r = 5.6);
							}
							translate(v = [12.000000000000002, 6.0, 0]) {
								cylinder(h = 0.4, r = 5.6);
							}
							translate(v = [-12.000000000000002, -6.0, 0]) {
								cylinder(h = 0.4, r = 5.6);
							}
							translate(v = [12.000000000000002, -6.0, 0]) {
								cylinder(h = 0.4, r = 5.6);
							}
						}
						translate(v = [0, 0, 9.6]) {
							hull() {
								translate(v = [-12.000000000000002, 6.0, 0]) {
									cylinder(h = 0.4, r = 5.6);
								}
								translate(v = [12.000000000000002, 6.0, 0]) {
									cylinder(h = 0.4, r = 5.6);
								}
								translate(v = [-12.000000000000002, -6.0, 0]) {
									cylinder(h = 0.4, r = 5.6);
								}
								translate(v = [12.000000000000002, -6.0, 0]) {
									cylinder(h = 0.4, r = 5.6);
								}
							}
						}
						translate(v = [17.6, 6.0, 0.40000000000000036]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 0.4);
							}
						}
						translate(v = [-17.6, 6.0, 0.40000000000000036]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 0.4);
							}
						}
						translate(v = [17.6, 6.0, 9.6]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 0.4);
							}
						}
						translate(v = [-17.6, 6.0, 9.6]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 0.4);
							}
						}
						translate(v = [-12.0, 11.6, 0.40000000000000036]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 0.4);
							}
						}
						translate(v = [-12.0, -11.6, 0.40000000000000036]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 0.4);
							}
						}
						translate(v = [-12.0, 11.6, 9.600000000000001]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 0.4);
							}
						}
						translate(v = [-12.0, -11.6, 9.600000000000001]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 0.4);
							}
						}
						translate(v = [-12.0, -6.0, 0.4]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [12.0, -6.0, 0.4]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [12.0, 6.0, 0.4]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [-12.0, 6.0, 0.4]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [-12.0, -6.0, 9.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [12.0, -6.0, 9.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [12.0, 6.0, 9.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [-12.0, 6.0, 9.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
						translate(v = [-12.0, -6.0, 0.4]) {
							rotate_extrude(angle = 360) {
								translate(v = [5.6000000000000005, 0, 0]) {
									circle(r = 0.4);
								}
							}
						}
					}
					union();
				}
			}
		}
	}
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-12.0, 5.999999999999999, 0]) {
								cylinder(h = 10.2, r = 5.2);
							}
							translate(v = [12.0, 5.999999999999999, 0]) {
								cylinder(h = 10.2, r = 5.2);
							}
							translate(v = [-12.0, -5.999999999999999, 0]) {
								cylinder(h = 10.2, r = 5.2);
							}
							translate(v = [12.0, -5.999999999999999, 0]) {
								cylinder(h = 10.2, r = 5.2);
							}
						}
					}
					union();
				}
			}
		}
	}
}
