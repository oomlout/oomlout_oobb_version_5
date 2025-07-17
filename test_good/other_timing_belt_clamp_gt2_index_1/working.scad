$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, -1.5000000000]) {
			hull() {
				translate(v = [-19.0000000000, 19.0000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
				translate(v = [19.0000000000, 19.0000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
				translate(v = [-19.0000000000, -19.0000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
				translate(v = [19.0000000000, -19.0000000000, 0]) {
					cylinder(h = 3, r = 5);
				}
			}
		}
	}
	union() {
		translate(v = [15, 7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.8000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [15, -7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.8000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, 7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.8000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, -7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.8000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15, 7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.8000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15, -7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.8000000000);
						}
					}
					union();
				}
			}
		}
	}
}