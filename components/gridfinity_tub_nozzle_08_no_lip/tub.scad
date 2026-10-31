// Standard Gridfinity feet and single M3 label interface, with an optional shallow guide.
use <../gridfinity_tray_quarter_increment/gridfinity_tray_quarter_increment.scad>
use <label_interface.scad>

module gridfinity_tub_nozzle_08(
    gridfinity_width=2, gridfinity_height=1, gridfinity_depth=16.5/7,
    lipped=false, wall_thickness=0.9, floor_thickness=1.0,
    label_corner=0, label_offset=-1, label_lift=undef, fn=64) {
    effective_lift=is_undef(label_lift)?(lipped?-2.15:0):label_lift;
    w=gridfinity_width; h=gridfinity_height; d=gridfinity_depth*7;
    assert(w>=0.5 && h>=0.5 && d>=16.5);
    assert(wall_thickness>=0.8 && wall_thickness<=1.6);
    assert(floor_thickness>=0.8 && floor_thickness<=2);
    module mount() {
        tl_at_corners(w,h,d,corners=[label_corner])
            translate([label_offset,0,effective_lift]) children();
    }
    difference() {
        union() {
            gridfinity_tray_quarter_increment(
                gridfinity_width=w, gridfinity_height=h, gridfinity_depth=gridfinity_depth,
                wall_thickness=wall_thickness, floor_thickness=floor_thickness,
                efficient_floor="on", lip_style="none",
                lip_top_notches=false, headroom=0.8, height_includes_lip=false,
                label_style="disabled", enable_magnets=false, enable_screws=false,
                cavity_floor_radius=0, render_position="center", fn=fn);
            if (lipped) shallow_guide(w,h,d,wall_thickness,fn);
            mount() if (lipped) intersection() {
                tl_receiver();
                // Supported local receiver: preserve the standard feet below Z=5.
                start = 5-(d-10.2+effective_lift);
                translate([-5,0,0]) rotate([90,0,90]) linear_extrude(height=10)
                    polygon([[-2,start],[wall_thickness-1.6,start],
                        [5,start+6.6-wall_thickness],[5,30],[-2,30]]);
            } else tl_receiver();
        }
        mount() tl_mount_holes();
        if (lipped) guide_top_cut(w,h,d,fn);
    }
}

// Full original upper chamfer, with a 45-degree underside back to the thin wall.
module guide_taper(w,h,r1,r2,z,height,fn) {
    hull() for(x=[-w*21+4,w*21-4],y=[-h*21+4,h*21-4])
        translate([x,y,z]) cylinder(r1=r1,r2=r2,h=height,$fn=fn);
}

module guide_top_cut(w,h,d,fn) {
    // 1.9 mm wall at d-1.2; 0.7 mm at the nominal top, matching the original lip.
    guide_taper(w,h,3.75-1.9,3.75-0.7+0.02,d-1.2,1.22,fn);
}

module shallow_guide(w,h,d,wall,fn) {
    peak=d-1.2;
    underside=1.9-wall;
    flat_height=0.4;
    lower=peak-flat_height;
    z0=lower-underside;
    difference() {
        guide_taper(w,h,3.75,3.75,z0,d-0.01-z0,fn);
        guide_taper(w,h,3.75-wall+0.01,3.75-1.9,z0-0.01,underside+0.01,fn);
        // Overlap the cutter joins inside the adjacent voids for taller trays;
        // this avoids coplanar slivers without changing the finished profile.
        join_overlap=d>16.5 ? 0.01 : 0;
        guide_taper(w,h,3.75-1.9,3.75-1.9,lower-join_overlap,flat_height+2*join_overlap,fn);
        guide_top_cut(w,h,d,fn);
    }
}
