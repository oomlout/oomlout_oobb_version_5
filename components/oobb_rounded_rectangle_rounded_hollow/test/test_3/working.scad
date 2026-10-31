$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0.6]) {
							hull() {
								translate(v = [-10.0, 5.0, 0]) {
									cylinder(h = 6.8, r = 5);
								}
								translate(v = [10.0, 5.0, 0]) {
									cylinder(h = 6.8, r = 5);
								}
								translate(v = [-10.0, -5.0, 0]) {
									cylinder(h = 6.8, r = 5);
								}
								translate(v = [10.0, -5.0, 0]) {
									cylinder(h = 6.8, r = 5);
								}
							}
						}
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 0.6, r = 4.4);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 0.6, r = 4.4);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 0.6, r = 4.4);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 0.6, r = 4.4);
							}
						}
						translate(v = [0, 0, 7.4]) {
							hull() {
								translate(v = [-10.0, 5.0, 0]) {
									cylinder(h = 0.6, r = 4.4);
								}
								translate(v = [10.0, 5.0, 0]) {
									cylinder(h = 0.6, r = 4.4);
								}
								translate(v = [-10.0, -5.0, 0]) {
									cylinder(h = 0.6, r = 4.4);
								}
								translate(v = [10.0, -5.0, 0]) {
									cylinder(h = 0.6, r = 4.4);
								}
							}
						}
						translate(v = [14.4, 5.0, 0.5999999999999996]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 0.6);
							}
						}
						translate(v = [-14.4, 5.0, 0.5999999999999996]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 0.6);
							}
						}
						translate(v = [14.4, 5.0, 7.399999999999999]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 0.6);
							}
						}
						translate(v = [-14.4, 5.0, 7.399999999999999]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 0.6);
							}
						}
						translate(v = [-10.0, 9.4, 0.5999999999999996]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 0.6);
							}
						}
						translate(v = [-10.0, -9.4, 0.5999999999999996]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 0.6);
							}
						}
						translate(v = [-10.0, 9.4, 7.399999999999999]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 0.6);
							}
						}
						translate(v = [-10.0, -9.4, 7.399999999999999]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 0.6);
							}
						}
						translate(v = [-10.0, -5.0, 0.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [10.0, -5.0, 0.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [10.0, 5.0, 0.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [-10.0, 5.0, 0.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [-10.0, -5.0, 7.3999999999999995]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [10.0, -5.0, 7.3999999999999995]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [10.0, 5.0, 7.3999999999999995]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [-10.0, 5.0, 7.3999999999999995]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
								}
							}
						}
						translate(v = [-10.0, -5.0, 0.6]) {
							rotate_extrude(angle = 360) {
								translate(v = [4.3999999999999995, 0, 0]) {
									circle(r = 0.6);
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
							translate(v = [-10.0, 5.000000000000001, 0]) {
								cylinder(h = 6.6, r = 3.8);
							}
							translate(v = [10.0, 5.000000000000001, 0]) {
								cylinder(h = 6.6, r = 3.8);
							}
							translate(v = [-10.0, -5.000000000000001, 0]) {
								cylinder(h = 6.6, r = 3.8);
							}
							translate(v = [10.0, -5.000000000000001, 0]) {
								cylinder(h = 6.6, r = 3.8);
							}
						}
					}
					union();
				}
			}
		}
	}
}
