module oobb_surface_1559f0ae4a34_raw() {
    translate([0, 0, -0.75])
        scale([0.035, 0.035, 0.015])
            surface(file = "icon_1000px_ea079e4b2913.png", center = true, invert = true, convexity = 10);
}

module oobb_surface_1559f0ae4a34() {
    rotate([0, 0, 0]) {
        difference() {
            oobb_surface_1559f0ae4a34_raw();
            translate([-18.5, -18.5, -1.4985])
                cube([37, 37, 1.0015], center = false);
        }
    }
}
