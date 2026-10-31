// Compact pull-in M3 interface. Local +Y goes from outside wall into the bin.
// The nut loads THROUGH the accessory and is drawn toward -Y by the screw.
// Standard DIN934 M3: 5.5 mm AF, 2.4 mm thick; no nyloc nuts.
function tl_top() = 8.4;
function tl_plate_top() = 10;
function tl_screw_z() = 4.4;
module tl_y_hole(d=3.8,y=-3,length=16,z=4.4) {
    translate([0,y,z]) rotate([-90,0,0]) cylinder(d=d,h=length,$fn=48);
}
module tl_hex(af=5.8,y=3,length=5.4) {
    translate([0,y+length,4.4]) rotate([90,0,0]) linear_extrude(height=length)
        rotate(30) circle(r=af/sqrt(3),$fn=6);
}
module tl_nut_void(af_clearance=0.30,thickness_clearance=0.40) {
    w=5.5+af_clearance;
    t=2.4+thickness_clearance;
    // Ease insertion independently of the snug, anti-rotation pull-in seat.
    // Default straight loading slot: 6.2 x 3.2mm (was 5.8 x 2.8mm).
    loading_w=w+0.40;
    loading_t=t+0.40;
    assert(af_clearance>=0.15 && af_clearance<=0.45);
    assert(thickness_clearance>=0.2 && thickness_clearance<=0.6);
    // Closed hexagonal pull-in seat, followed by the open loading bay.
    tl_hex(af=w,y=3,length=2.6+t);
    // Keep screw alignment; 0.02mm relief avoids coincident faces with the seat.
    bottom=4.4-w/sqrt(3)-0.02;
    translate([0,5.6+loading_t,0]) rotate([90,0,0]) linear_extrude(height=loading_t)
        polygon([[-loading_w/2,bottom+loading_w/(2*sqrt(3))],[0,bottom],
                 [loading_w/2,bottom+loading_w/(2*sqrt(3))],
                 [loading_w/2,11],[-loading_w/2,11]]);
    hull() {
        translate([-loading_w/2+0.1,5.7,9.35])
            cube([loading_w-0.2,loading_t-0.2,0.01]);
        translate([-loading_w/2-0.4,5.2,10.01])
            cube([loading_w+0.8,loading_t+0.8,0.01]);
    }
    tl_y_hole();
}
module tl_mount_holes() {
    tl_y_hole();
    // 90-degree countersink for a flush M3 countersunk screw (6 mm head).
    translate([0,-1.61,4.4]) rotate([-90,0,0])
        cylinder(d1=6.4,d2=3.8,h=1.3,$fn=48);
}
module tl_receiver() {
    difference() {
        union() {
            // Only a 1.4mm inward wall reinforcement, no fixed nut cage.
            translate([-4.8,-1.6,0]) cube([9.6,3,8.4]);
            translate([-4.8,0,0]) rotate([90,0,90]) linear_extrude(height=9.6)
                // Shorten the lower tip to clear the lip of stacked 18mm bins.
                // The first 0.4mm projects by one extrusion; the rest is 45deg.
                polygon([[0,-1],[0.4,-1],[1.4,0],[0,0]]);
            // Two tiny locating keys: lead-in underneath, horizontal stops above.
            for(x=[-3.2,3.2]) translate([x-0.6,0,0]) rotate([90,0,90])
                linear_extrude(height=1.2)
                    polygon([[1.3,4.7],[2.6,6],[2.6,7.4],[1.3,7.4]]);
        }
        tl_mount_holes();
    }
}
module tl_rounded_plate(w,d,h=1.6,r=0.8) {
    linear_extrude(height=h) hull()
        for(x=[r,w-r],y=[r,d-r]) translate([x,y]) circle(r=r,$fn=24);
}
module tl_accessory(label=true,af_clearance=0.30,thickness_clearance=0.40,
                    plate_width=undef,plate_height=undef) {
    w=is_undef(plate_width)?(label?42.1:10):plate_width;
    d=is_undef(plate_height)?(label?29.4:10):plate_height;
    assert(w>=10 && d>=10,"Accessory plate must cover the 10mm attachment.");
    difference() {
        union() {
            // Add a 2.7mm side flange to meet the rim with ~0.25mm clearance.
            // plate_width is the original label area; flange is additional.
            // Keep the far edge, mounting keys and current stacking height fixed.
            side_flange=label?2.7:0;
            translate([label?-4.3-side_flange:-w/2,1.6,8.4])
                tl_rounded_plate(w+side_flange,d);
            // Nut cage is part of the REMOVABLE accessory, tucked underneath.
            translate([-4.3,1.6,0]) cube([8.6,8,8.5]);
        }
        tl_nut_void(af_clearance,thickness_clearance);
        for(x=[-3.2,3.2]) translate([x-0.85,1.39,-0.1])
            cube([1.7,1.46,7.5]);
    }
}
module tl_accessory_print(label=true,af_clearance=0.30,thickness_clearance=0.40,
                          plate_width=undef,plate_height=undef) {
    translate([0,0,10]) rotate([180,0,0])
        tl_accessory(label,af_clearance,thickness_clearance,plate_width,plate_height);
}
// Nutless spacer: the existing locator-key slots seat on the bin mount.
// Keys project 2.6mm inward. The first bead starts at 2.85mm for 0.25mm
// clearance, also clearing the rim. The spacer starts at 1.6mm: 1.25mm thick.
function tl_bead_start() = 2.85;
function tl_bead_adapter_thickness() = tl_bead_start()-1.6;
module tl_bead_adapter() {
    difference() {
        translate([-5,1.6,0]) cube([10,tl_bead_adapter_thickness(),10]);
        tl_y_hole(d=3.4);
        for(x=[-3.2,3.2]) translate([x-0.85,1.39,-0.1])
            // Slots pass fully through the slim spacer: no coincident skin.
            cube([1.7,tl_bead_adapter_thickness()+0.4,7.5]);
    }
}
module tl_bead_adapter_print() {
    // Broad face on bed: the 1.25mm spacer prints flat, like the colour beads.
    translate([0,10,-1.6]) rotate([90,0,0]) tl_bead_adapter();
}
// Local Y=0..3 is the stacking direction. The final bead alone holds a nut.
// Left edge follows the adjacent wall's lower rim bevel with >=0.25mm relief.
// The foot extends underneath the lip: slide in along the side before clamping.
module tl_bead() {
    difference() {
        translate([0,3,0]) rotate([90,0,0]) linear_extrude(height=3)
            polygon([[-7.55,0],[5,0],[5,10],[-7.1,10],
                     [-7.1,8.8],[-8.15,7.75],[-8.15,0.6]]);
        tl_y_hole(d=3.4,y=-0.1,length=3.2);
        // 5.9mm AF, 2.6mm deep; 0.4mm back wall, open outer face.
        tl_hex(af=5.9,y=0.4,length=2.7);
    }
}
module tl_bead_print() {
    // Closed face on bed; nut pocket faces up, no bridging or support.
    rotate([-90,0,0]) mirror([0,1,0]) tl_bead();
}
module tl_bead_stack(count=3) {
    tl_bead_adapter();
    for(i=[0:count-1]) translate([0,tl_bead_start()+3*i,0]) tl_bead();
}
module tl_at_corners(nx=2,ny=2,body_height=38.5,corners=undef) {
    assert(nx>=0.5 && ny>=0.5 && body_height>=14.3);
    sites=is_undef(corners)?(nx<1?[1,3]:ny<1?[0,2]:[0,1,2,3]):corners;
    positions=[[-nx*21+10.25,-ny*21+1.85], [nx*21-1.85,-ny*21+10.25],
               [nx*21-10.25,ny*21-1.85], [-nx*21+1.85,ny*21-10.25]];
    for(i=sites) translate([positions[i][0],positions[i][1],body_height-10.2])
        rotate([0,0,90*i]) children();
}
module tl_nut_reference(y=3,af=5.5) {
    color("silver") difference() {
        tl_hex(af=af,y=y,length=2.4);
        tl_y_hole(d=3);
    }
}
module tl_screw_reference() {
    // M3 x 10 countersunk, overall length including head.
    color("silver") {
        tl_y_hole(d=3,y=-0.1,length=8.5);
        translate([0,-1.6,4.4]) rotate([-90,0,0])
            cylinder(d1=6,d2=3,h=1.5,$fn=48);
    }
}
