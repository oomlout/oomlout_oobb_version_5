include <components/github_belfry_bosl2_gear/BOSL2/std.scad>;
include <components/github_belfry_bosl2_gear/BOSL2/gears.scad>;

module github_belfry_bosl2_gear_raw(
    teeth=16,
    mod=2,
    thickness=8,
    shaft_diam=0,
    pressure_angle=20,
    backlash=0,
    helical=0,
    herringbone=false,
    gear_spin=0
) {
    spur_gear(
        mod=mod,
        teeth=teeth,
        thickness=thickness,
        shaft_diam=shaft_diam,
        pressure_angle=pressure_angle,
        backlash=backlash,
        helical=helical,
        herringbone=herringbone,
        gear_spin=gear_spin,
        anchor=CENTER
    );
}
