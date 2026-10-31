use <../gridfinity_tray_quarter_increment/gridfinity_tray_quarter_increment.scad>

// Radius-offset rectangle in a plane, extruded from z for h millimetres.
module _rounded_prism(x,y,r,z,h) {
    translate([0,0,z]) linear_extrude(height=h)
        offset(r=r) square([max(0.1,x-2*r),max(0.1,y-2*r)],center=true);
}

module _rounded_taper(x1,y1,x2,y2,r,z,h) {
    hull() {
        _rounded_prism(x1,y1,r,z,0.02);
        _rounded_prism(x2,y2,r,z+h-0.02,0.02);
    }
}

module base_plate(w,h,base_top,base_bridge_mm,gf_width,gf_height) {
    union() {
        intersection() {
            gridfinity_tray_quarter_increment(gridfinity_width=gf_width,
                gridfinity_height=gf_height,gridfinity_depth=1,
                floor_thickness=0.7,wall_thickness=0,efficient_floor="off",
                lip_style="none",enable_magnets=false,enable_screws=false,
                filled_in="disabled",align_grid_x="near",align_grid_y="near");
            translate([-w,-h,-0.01]) cube([2*w,2*h,4.75+0.01]);
        }
        // Solid bridge closes inter-cell clearance while keeping standard feet.
        _rounded_prism(w,h,3.75,4.75,base_bridge_mm);
    }
}

module inset_wall(w,h,inset,corner,base_top,wall_top) {
    _rounded_prism(w-2*inset,h-2*inset,corner,base_top,wall_top-base_top);
}

module flare(w,h,inset,corner,z,height) {
    if(height>0)
        _rounded_taper(w-2*inset,h-2*inset,w,h,corner,z,height);
}

module upper_wall(w,h,corner,z,height) {
    _rounded_prism(w,h,corner,z,max(0.02,height));
}

module wall_cavity(w,h,inset,wall,corner,base_top,flare_z,flare_height,height) {
    union() {
        _rounded_prism(w-2*inset-2*wall,h-2*inset-2*wall,
            max(0.2,corner-wall),base_top,max(0.02,height-base_top+0.1));
        if(flare_height>0)
            _rounded_taper(w-2*inset-2*wall,h-2*inset-2*wall,
                w-2*wall,h-2*wall,max(0.2,corner-wall),flare_z,flare_height);
        // Keep the upper wall cavity at full width after the flare completes.
        _rounded_prism(w-2*wall,h-2*wall,max(0.2,corner-wall),
            flare_z+flare_height,max(0.02,height-flare_z-flare_height+0.1));
    }
}

// Shallow receiver lip derived from the nozzle_08 Gridfinity guide profile.
module guide_taper(w,h,r1,r2,z,height,corner=3.75) {
    hull()
        for(x=[-w/2+corner,w/2-corner],y=[-h/2+corner,h/2-corner])
            translate([x,y,z]) cylinder(r1=r1,r2=r2,h=height,$fn=64);
}

module mating_lip(w,h,wall,corner,top) {
    flat_height=0.4;
    peak=top-1.2;
    underside=1.9-wall;
    lower=peak-flat_height;
    z0=lower-underside;
    difference() {
        guide_taper(w,h,corner,corner,z0,top-0.01-z0,corner);
        guide_taper(w,h,corner-wall+0.01,corner-1.9,z0-0.01,
            underside+0.01,corner);
        guide_taper(w,h,corner-1.9,corner-1.9,lower,flat_height,corner);
    }
}

module guide_top_cut(w,h,corner,top) {
    // Receiver opening expands outward at 45 degrees over the final 1.22 mm.
    guide_taper(w,h,corner-1.9,corner-0.7+0.02,top-1.2,1.22,corner);
}

module label_support(w,h,size,wall,z,thickness,support_drop,outer_margin=1.25) {
    if(size>wall) {
        x0=w/2-size-outer_margin;
        y0=h/2-size-outer_margin;
        // Carry the diagonal down to the end of the straight upper wall.
        hull() {
            translate([w/2-wall-0.05,y0,z-thickness-support_drop])
                cube([wall+0.1,size-wall,0.02]);
            translate([x0,h/2-wall-0.05,z-thickness-support_drop])
                cube([size-wall,wall+0.1,0.02]);
            translate([x0,y0,z-thickness]) cube([size,size,0.02]);
        }
    }
}

module label_pad_corner(w,h,size,z,wall=1.2,thickness=0.4,corner=3.75,
    base_top=5.75,inset=5,flare_start=5.75,flare_height=5,
    flare_end=10.75,height=17,outer_margin=1.25) {
    if(size>0) {
        // A 45-degree printable gusset reaches down into the outward flare.
        support_run=max(0,(size-wall)/2);
        support_drop=min(support_run,z-thickness-base_top);
        x0=w/2-size-outer_margin;
        y0=h/2-size-outer_margin;
        intersection() {
            union() {
                label_support(w,h,size,wall,z,thickness,support_drop,outer_margin);
                translate([x0,y0,z-thickness])
                    cube([size,size,thickness]);
            }
            // Keep the gusset inside the curved, tapered exterior at every Z.
            union() {
                inset_wall(w,h,inset,corner,base_top,height);
                flare(w,h,inset,corner,flare_start,flare_height);
                upper_wall(w,h,corner,flare_end,height-flare_end);
            }
        }
    }
}

module label_pad(w,h,size,z,wall=1.2,thickness=0.4,corner=3.75,
    base_top=5.75,inset=5,flare_start=5.75,flare_height=5,
    flare_end=10.75,height=17,outer_margin=1.25) {
    if(size>0)
        for(sx=[-1,1],sy=[-1,1])
            scale([sx,sy,1])
                label_pad_corner(w,h,size,z,wall,thickness,corner,
                    base_top,inset,flare_start,flare_height,flare_end,height,
                    outer_margin);
}

module gridfinity_palet_pot(gridfinity_width=1,gridfinity_height=1,height_mm=17,
    inset_mm=5,flare_from_top_mm=12,wall_thickness=1.2,label_size=10,
    label_drop_mm=5.75,base_bridge_mm=1) {
    w=gridfinity_width*42-0.5; h=gridfinity_height*42-0.5;
    base_top=4.75+base_bridge_mm;
    flare_start=max(base_top,height_mm-flare_from_top_mm);
    flare_height=min(inset_mm,height_mm-flare_start);
    flare_end=flare_start+flare_height;
    corner=3.75;
    assert(w>2*inset_mm+2*wall_thickness && h>2*inset_mm+2*wall_thickness);
    assert(wall_thickness<1.9);
    assert(height_mm>=base_top+inset_mm);
    assert(label_drop_mm>=0 && height_mm-label_drop_mm>base_top);
    assert(base_bridge_mm>0);
    render() union() {
        // Standard feet with an uninterrupted base plate.
        base_plate(w,h,base_top,base_bridge_mm,gridfinity_width,gridfinity_height);
        // Separate named wall zones share the same 45-degree transition.
        difference() {
            union() {
                union() {
                    inset_wall(w,h,inset_mm,corner,base_top,height_mm);
                    flare(w,h,inset_mm,corner,flare_start,flare_height);
                    upper_wall(w,h,corner,flare_end,height_mm-flare_end);
                }
                mating_lip(w,h,wall_thickness,corner,height_mm);
            }
            // Hollow the pot, then shape the mating receiver into the rim.
            wall_cavity(w,h,inset_mm,wall_thickness,corner,base_top,
                flare_start,flare_height,height_mm);
            guide_top_cut(w,h,corner,height_mm);
        }
        // Recess pads below the rim and lip; each has a full 10 x 10 mm face.
        label_pad(w,h,label_size,height_mm-label_drop_mm,wall_thickness,0.4,
            corner,base_top,inset_mm,flare_start,flare_height,flare_end,height_mm,
            1.25);
    }
}


// Top pickup for gridfinity_palet_pot.
// The Gridfinity foot datum aligns on the pot rim; a separate twist rotor
// deploys four flexible hooks under the corner label tabs.
module _tp_round_xy(w,h,r,z,t) {
    translate([0,0,z]) linear_extrude(height=t)
        offset(r=r) square([max(0.1,w-2*r),max(0.1,h-2*r)],center=true);
}

module _tp_taper_foot(cx,cy,bottom,top,z,height,clearance) {
    hull() {
        translate([cx,cy,0]) _tp_round_xy(bottom-2*clearance,bottom-2*clearance,2.2,z,0.02);
        translate([cx,cy,0]) _tp_round_xy(top-2*clearance,top-2*clearance,3.75,z+height-0.02,0.02);
    }
}

module _tp_gridfinity_base(width,height,clearance,rim_z) {
    pitch=42; foot_h=4.75; foot_bottom=35.6; foot_top=41.5;
    outer_w=width*pitch-0.5; outer_h=height*pitch-0.5;
    union() {
        for(ix=[0:width-1],iy=[0:height-1])
            _tp_taper_foot((ix-(width-1)/2)*pitch,(iy-(height-1)/2)*pitch,
                foot_bottom,foot_top,rim_z-foot_h,foot_h,clearance);
        _tp_round_xy(outer_w-2*clearance,outer_h-2*clearance,3.75,
            rim_z+0.02,1.3);
        translate([0,0,rim_z-foot_h-0.01])
            cylinder(d=6.5,h=foot_h+1.33,$fn=64);
    }
}

module _tp_base_with_guide(width,height,clearance,height_mm,label_drop_mm) {
    tab_under=height_mm-label_drop_mm-0.4;
    // Keep the sleeve above the rotating hooks, which sweep directly below
    // the label tabs. The rotor stem runs in the sleeve's clearance bore.
    guide_bottom=tab_under+0.1;
    difference() {
        union() {
            _tp_gridfinity_base(width,height,clearance,height_mm);
            translate([0,0,guide_bottom]) cylinder(d=10.4,
                h=height_mm-guide_bottom+0.02,$fn=64);
        }
        translate([0,0,guide_bottom-0.01]) cylinder(d=6.5,
            h=height_mm+1.32-guide_bottom,$fn=64);
    }
}

module _tp_rotor(width,height,label_size,label_drop_mm,height_mm,engaged,
    contact_overlap=0.05) {
    outer_w=width*42-0.5; outer_h=height*42-0.5;
    tab_under=height_mm-label_drop_mm-0.4;
    hook_t=1.0; hook_top=tab_under+contact_overlap; hook_z=hook_top-hook_t;
    arm_w=5.6;
    tab_outer=min(outer_w,outer_h)/2-1.25;
    engaged_arm_end=sqrt(2)*tab_outer-0.15;
    // The flexible arms remain inside the pot while lowering; twisting deploys them.
    stowed_arm_end=min(outer_w,outer_h)/2-label_size-2.0;
    arm_end=engaged?engaged_arm_end:stowed_arm_end;
    turn=engaged?45:0;
    knob_bottom=height_mm+1.35;
    union() {
        for(q=[0:3]) rotate([0,0,turn+q*90])
            translate([0,-arm_w/2,hook_z]) cube([arm_end,arm_w,hook_t]);
        translate([0,0,hook_z]) cylinder(d=5.8,h=knob_bottom-hook_z,$fn=64);
        translate([0,0,knob_bottom]) cylinder(d=16,h=1.6,$fn=64);
        translate([0,0,knob_bottom+1.58]) rotate([0,0,turn])
            translate([4.8,0,0.35]) cube([5.6,1.4,0.7],center=true);
    }
}

module gridfinity_top_pickup(gridfinity_width=1,gridfinity_height=1,
    height_mm=17,label_size=10,label_drop_mm=5.75,clearance_mm=0.5,
    engaged=false,draw_handle=true,print_layout=false,contact_overlap=0.05) {
    assert(clearance_mm>=0,"Pickup clearance cannot be negative.");
    assert(contact_overlap>=0,"Hook contact overlap cannot be negative.");
    assert(label_size>=8,"Label tabs are too small for the pickup hooks.");
    assert(gridfinity_width>=1 && gridfinity_height>=1,
        "Pickup supports one or more whole Gridfinity cells.");
    if(print_layout) {
        rotor_min=height_mm-label_drop_mm-0.4+contact_overlap-1.0;
        rotor_x=max(gridfinity_width*42,gridfinity_height*42)/2
            +sqrt(2)*(min(gridfinity_width*42-0.5,gridfinity_height*42-0.5)/2-1.25)+8;
        translate([0,0,1.32]) rotate([180,0,0])
            _tp_gridfinity_base(gridfinity_width,gridfinity_height,clearance_mm,0);
        translate([rotor_x,0,-rotor_min])
            _tp_rotor(gridfinity_width,gridfinity_height,label_size,
                label_drop_mm,height_mm,true,contact_overlap);
    } else {
        _tp_base_with_guide(gridfinity_width,gridfinity_height,clearance_mm,
            height_mm,label_drop_mm);
        _tp_rotor(gridfinity_width,gridfinity_height,label_size,label_drop_mm,
            height_mm,engaged,contact_overlap);
    }
}
