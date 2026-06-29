include <components/github_belfry_bosl2_gear/BOSL2/std.scad>;
include <components/github_belfry_bosl2_gear/BOSL2/gears.scad>;

module oobb_gear_spur_raw(
    teeth=16,
    gear_mod=2,
    thickness=8,
    shaft_diam=0,
    backlash=0,
    gear_bevel=0
) {
    cp     = gear_mod * PI;
    tip_r  = outer_radius(circ_pitch=cp, teeth=teeth);
    extra  = tip_r + gear_bevel + 2;
    half_t = thickness / 2;

    difference() {
        spur_gear(
            mod=gear_mod,
            teeth=teeth,
            thickness=thickness,
            shaft_diam=shaft_diam,
            pressure_angle=20,
            backlash=backlash,
            helical=0,
            herringbone=false,
            gear_spin=0,
            anchor=CENTER
        );
        if (gear_bevel > 0) {
            // top face chamfer — ring with conical inner edge
            translate([0, 0, half_t - gear_bevel])
            difference() {
                cylinder(r=extra, h=gear_bevel + 0.01);
                cylinder(r1=tip_r, r2=tip_r - gear_bevel, h=gear_bevel + 0.01);
            }
            // bottom face chamfer — mirror of top
            translate([0, 0, -half_t - 0.01])
            difference() {
                cylinder(r=extra, h=gear_bevel + 0.01);
                cylinder(r1=tip_r - gear_bevel, r2=tip_r, h=gear_bevel + 0.01);
            }
        }
    }
}
