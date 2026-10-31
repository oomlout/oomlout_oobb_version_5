include <C:/gh/oomlout_oobb_version_5/components/github_belfry_bosl2_gear/BOSL2/std.scad>
include <C:/gh/oomlout_oobb_version_5/components/github_belfry_bosl2_gear/BOSL2/gears.scad>

// BOSL2 VNFs use clockwise face winding. Keep every upward-facing or vertical
// working face, then close its silhouette vertically down to the print bed.
// This adds material below the existing bevel without stretching its tooth faces.
function _oobb_bevel_to_base(bare, bottom, chamfer) =
    let(
        faces = [for (f=bare[1])
            let(p=select(bare[0],f), n=cross(p[1]-p[0],p[2]-p[0]))
            if (n.z <= 1e-9) f],
        shell = [bare[0],faces],
        outlines = vnf_boundary(shell)
    )
    assert(len(outlines)==1, "Expected a single bevel tooth silhouette")
    let(
        path = outlines[0],
        count = len(path),
        radius = max([for (p=path) norm(point2d(p))]),
        rings = chamfer>0 ? 3 : 2,
        vertices = concat(path,
            [for (p=path) [p.x,p.y,bottom+chamfer]],
            chamfer>0 ? [for (p=path)
                [(1-chamfer/radius)*p.x,(1-chamfer/radius)*p.y,bottom]] : [],
            [[0,0,bottom]]),
        sides = [for (r=[0:rings-2], i=[0:count-1])
            let(a=r*count+i, b=r*count+(i+1)%count,
                c=(r+1)*count+i, d=(r+1)*count+(i+1)%count)
            each [[b,a,c],[b,c,d]]],
        cap = [for (i=[0:count-1])
            [(rings-1)*count+(i+1)%count,(rings-1)*count+i,rings*count]]
    )
    assert(bottom+chamfer < min([for (p=path) p.z]), "Chamfer must fit below the bevel teeth")
    vnf_join([shell,[vertices,concat(sides,cap)]]);

// True bevel teeth, not a scaled spur extrusion. All dimensions refer to the large end.
module oobb_gear_bevel_raw(teeth=20, mate_teeth=20, gear_mod=1.5, depth=9,
    face_width=4.5, shaft_diam=0, pressure_angle=20, backlash=0.2,
    clearance=0.375, gear_spin=0, anchor="center", teeth_to_base=true, base_chamfer=0.4) {
    bare = bevel_gear(mod=gear_mod, teeth=teeth, mate_teeth=mate_teeth,
        shaft_angle=90, face_width=face_width, backing=0,
        pressure_angle=pressure_angle, backlash=backlash, clearance=clearance,
        spiral=0, cutter_radius=0, gear_spin=gear_spin, anchor="pitchbase");
    bounds = pointlist_bounds(bare[0]);
    tooth_height = bounds[1].z - bounds[0].z;
    backing = depth - tooth_height;
    assert(backing > 0, "depth must exceed the complete tooth envelope");
    delta = atan(teeth/mate_teeth);
    apex = gear_mod*teeth/2/tan(delta);
    shift = anchor == "center" ? depth/2-bounds[1].z
          : anchor == "bottom" ? depth-bounds[1].z
          : anchor == "apex" ? -apex : 0;
    translate([0,0,shift])
      if (teeth_to_base)
        difference() {
            vnf_polyhedron(_oobb_bevel_to_base(bare,bounds[1].z-depth,base_chamfer),convexity=12);
            if (shaft_diam>0) cylinder(d=shaft_diam,h=4*(depth+apex),center=true);
        }
      else
        bevel_gear(mod=gear_mod, teeth=teeth, mate_teeth=mate_teeth,
            shaft_angle=90, face_width=face_width, backing=backing,
            cone_backing=false, shaft_diam=shaft_diam,
            pressure_angle=pressure_angle, backlash=backlash, clearance=clearance,
            spiral=0, cutter_radius=0, gear_spin=gear_spin, anchor="pitchbase");
}
