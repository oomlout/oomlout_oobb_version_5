module oobb_surface_ab15fbe710af_raw() {
    translate([0, 0, 0])
        scale([0.07, 0.035, 0.01])
            surface(file = "icon_1000px_ea079e4b2913.png", center = true, invert = true, convexity = 10);
}

module oobb_surface_ab15fbe710af() {
    rotate([0, 0, 0]) {
        difference() {
            oobb_surface_ab15fbe710af_raw();
            translate([-36, -18.5, -1.749])
                cube([72, 37, 1.001], center = false);
        }
    }
}
