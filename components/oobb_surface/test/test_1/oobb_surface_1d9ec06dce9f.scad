module oobb_surface_1d9ec06dce9f_raw() {
    translate([0, 0, 0])
        scale([0.06, 0.06, 0.01])
            surface(file = "icon_1000px_ea079e4b2913.png", center = true, invert = true, convexity = 10);
}

module oobb_surface_1d9ec06dce9f() {
    rotate([0, 0, 0]) {
        difference() {
            oobb_surface_1d9ec06dce9f_raw();
            translate([-31, -31, -1.749])
                cube([62, 62, 1.001], center = false);
        }
    }
}
