// HTD5M polygon inherited from the bundled pulley_gt2.scad library.
// Parametric Pulley by droftarts (January 2012), updated by Oscar (January 2018).
// Original DXF tooth data: SDP/SI via oem.cadregister.com; see pulley_gt2.scad.
// A tooth-only primitive: the OOBB body supplies bores, flanges and hardware.
module pulley_htd5m(number_of_teeth=24, depth=15,
                    tooth_width_clearance=0.2, tooth_depth_clearance=0) {
    assert(number_of_teeth >= 8 && floor(number_of_teeth) == number_of_teeth);
    assert(depth > 0);
    assert(tooth_width_clearance >= 0 && tooth_width_clearance <= 0.5);
    assert(tooth_depth_clearance >= 0 && tooth_depth_clearance <= 0.3);
    outside_radius = number_of_teeth * 5 / (2 * PI) - 0.5715;
    tooth_width = 3.781;
    tooth_depth = 2.199;
    groove_origin = sqrt(pow(outside_radius, 2) - pow((tooth_width + tooth_width_clearance) / 2, 2));
    difference() {
        cylinder(r=outside_radius, h=depth, $fn=number_of_teeth * 20);
        for (i=[0:number_of_teeth-1]) {
            rotate([0, 0, i * 360 / number_of_teeth])
                translate([0, -groove_origin, -0.01])
                    scale([(tooth_width + tooth_width_clearance) / tooth_width,
                           (tooth_depth + tooth_depth_clearance) / tooth_depth, 1])
                        linear_extrude(height=depth + 0.02)
                            polygon([[-1.89036,-0.75],[-1.89036,0],[-1.741168,0.02669],[-1.61387,0.100806],[-1.518984,0.21342],[-1.467026,0.3556],[-1.427162,0.960967],[-1.398568,1.089602],[-1.359437,1.213531],[-1.310296,1.332296],[-1.251672,1.445441],[-1.184092,1.552509],[-1.108081,1.653042],[-1.024167,1.746585],[-0.932877,1.832681],[-0.834736,1.910872],[-0.730271,1.980701],[-0.62001,2.041713],[-0.504478,2.09345],[-0.384202,2.135455],[-0.259708,2.167271],[-0.131524,2.188443],[-0.000176,2.198511],[0.131296,2.188504],[0.259588,2.167387],[0.384174,2.135616],[0.504527,2.093648],[0.620123,2.04194],[0.730433,1.980949],[0.834934,1.911132],[0.933097,1.832945],[1.024398,1.746846],[1.108311,1.653291],[1.184308,1.552736],[1.251865,1.445639],[1.310455,1.332457],[1.359552,1.213647],[1.39863,1.089664],[1.427162,0.960967],[1.467026,0.3556],[1.518984,0.21342],[1.61387,0.100806],[1.741168,0.02669],[1.89036,0],[1.89036,-0.75]]);
        }
    }
}
