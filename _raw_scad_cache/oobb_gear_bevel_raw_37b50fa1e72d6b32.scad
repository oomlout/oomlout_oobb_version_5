include <C:/gh/oomlout_oobb_version_5/components/github_belfry_bosl2_gear/BOSL2/std.scad>
include <C:/gh/oomlout_oobb_version_5/components/github_belfry_bosl2_gear/BOSL2/gears.scad>

function oobb_gear_bevel_face_width(teeth=40,mate_teeth=40,gear_mod=1.5,depth=9,clearance=0.375) =
    let(delta=atan(teeth/mate_teeth),R=gear_mod*teeth/2/sin(delta),d=gear_mod+clearance)
    (depth+(gear_mod+d)*sin(delta))/(cos(delta)+d*sin(delta)/R)+0.2;

// Measure the outer heel separately so the whole visible side is bevelled.
// This also gives callers a common reference for positioning centered STLs.
function oobb_gear_bevel_base_z(teeth=40,mate_teeth=40,gear_mod=1.5,
    pressure_angle=20,backlash=0.2,clearance=0.375,gear_spin=0) =
    let(heel=bevel_gear(mod=gear_mod,teeth=teeth,mate_teeth=mate_teeth,
        shaft_angle=90,face_width=0.0001,backing=0,spiral=0,cutter_radius=0,
        pressure_angle=pressure_angle,backlash=backlash,clearance=clearance,
        gear_spin=gear_spin,anchor="pitchbase"))
    pointlist_bounds(heel[0])[1].z;

module oobb_gear_bevel_raw(teeth=40,mate_teeth=40,gear_mod=1.5,depth=9,
    face_width=undef,shaft_diam=0,pressure_angle=20,backlash=0.2,
    clearance=0.375,gear_spin=0,anchor="center",base_chamfer=undef) {
    fw=is_undef(face_width) ? oobb_gear_bevel_face_width(teeth,mate_teeth,gear_mod,depth,clearance) : face_width;
    chamfer=is_undef(base_chamfer) ? gear_mod*8/15 : base_chamfer;
    bare=bevel_gear(mod=gear_mod,teeth=teeth,mate_teeth=mate_teeth,
        shaft_angle=90,face_width=fw,backing=0,spiral=0,cutter_radius=0,
        pressure_angle=pressure_angle,backlash=backlash,clearance=clearance,
        gear_spin=gear_spin,anchor="pitchbase");
    base=oobb_gear_bevel_base_z(teeth,mate_teeth,gear_mod,
        pressure_angle,backlash,clearance,gear_spin);
    delta=atan(teeth/mate_teeth);
    apex=gear_mod*teeth/2/tan(delta);
    shift=anchor=="center" ? -base-depth/2
         : anchor=="bottom" ? -base
         : anchor=="apex" ? -apex : 0;
    extent=2*(gear_mod*teeth+depth);
    foot=chamfer>0 ? projection(bare,cut=true,z=base+0.0001) : [];
    translate([0,0,shift])
      difference() {
        intersection() {
            vnf_polyhedron(bare,convexity=12);
            translate([-extent,-extent,base]) cube([2*extent,2*extent,depth]);
            if(chamfer>0)
                translate([0,0,base])
                    offset_sweep(simplify_path(foot[0],maxerr=gear_mod/150),
                        height=depth,bottom=os_chamfer(width=chamfer),anchor="base");
        }
        if(shaft_diam>0) cylinder(d=shaft_diam,h=4*(depth+apex),center=true);
      }
}
