$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 14]) {
			rotate(a = [180, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								hull() {
									difference() {
										union() {
											translate(v = [0, 0, 7.8]) {
												hull() {
													translate(v = [-14.0, 14.0, 0]) {
														cylinder(h = 0.2, r = 4);
													}
													translate(v = [14.0, 14.0, 0]) {
														cylinder(h = 0.2, r = 4);
													}
													translate(v = [-14.0, -14.0, 0]) {
														cylinder(h = 0.2, r = 4);
													}
													translate(v = [14.0, -14.0, 0]) {
														cylinder(h = 0.2, r = 4);
													}
												}
											}
											translate(v = [0, 0, 13.8]) {
												hull() {
													translate(v = [-23.5, 23.5, 0]) {
														cylinder(h = 0.2, r = 8);
													}
													translate(v = [23.5, 23.5, 0]) {
														cylinder(h = 0.2, r = 8);
													}
													translate(v = [-23.5, -23.5, 0]) {
														cylinder(h = 0.2, r = 8);
													}
													translate(v = [23.5, -23.5, 0]) {
														cylinder(h = 0.2, r = 8);
													}
												}
											}
										}
										union();
									}
								}
							}
						}
						hull() {
							translate(v = [-14.0, 14.0, 0]) {
								cylinder(h = 8, r = 4);
							}
							translate(v = [14.0, 14.0, 0]) {
								cylinder(h = 8, r = 4);
							}
							translate(v = [-14.0, -14.0, 0]) {
								cylinder(h = 8, r = 4);
							}
							translate(v = [14.0, -14.0, 0]) {
								cylinder(h = 8, r = 4);
							}
						}
					}
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								hull() {
									difference() {
										union() {
											translate(v = [0, 0, 7.8]) {
												hull() {
													translate(v = [-14.0, 14.0, 0]) {
														cylinder(h = 0.2, r = 2.5);
													}
													translate(v = [14.0, 14.0, 0]) {
														cylinder(h = 0.2, r = 2.5);
													}
													translate(v = [-14.0, -14.0, 0]) {
														cylinder(h = 0.2, r = 2.5);
													}
													translate(v = [14.0, -14.0, 0]) {
														cylinder(h = 0.2, r = 2.5);
													}
												}
											}
											translate(v = [0, 0, 13.8]) {
												hull() {
													translate(v = [-23.5, 23.5, 0]) {
														cylinder(h = 0.4, r = 6.5);
													}
													translate(v = [23.5, 23.5, 0]) {
														cylinder(h = 0.4, r = 6.5);
													}
													translate(v = [-23.5, -23.5, 0]) {
														cylinder(h = 0.4, r = 6.5);
													}
													translate(v = [23.5, -23.5, 0]) {
														cylinder(h = 0.4, r = 6.5);
													}
												}
											}
										}
										union();
									}
								}
							}
						}
						translate(v = [0, 0, -0.1]) {
							hull() {
								translate(v = [-14.0, 14.0, 0]) {
									cylinder(h = 8.2, r = 2.5);
								}
								translate(v = [14.0, 14.0, 0]) {
									cylinder(h = 8.2, r = 2.5);
								}
								translate(v = [-14.0, -14.0, 0]) {
									cylinder(h = 8.2, r = 2.5);
								}
								translate(v = [14.0, -14.0, 0]) {
									cylinder(h = 8.2, r = 2.5);
								}
							}
						}
					}
				}
			}
		}
	}
	union();
}
