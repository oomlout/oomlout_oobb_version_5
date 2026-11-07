# Two-screw belt-end tensioner

Two identical end bodies and two identical clamp jaws terminate two belts.
Each body has a socket-head screw seat on one side of its loop and an M3
nut pocket on the other. Rotate the second end 180 degrees in XY to pair
the head seats with the opposite end's nut pockets. The draw screws point
in opposite directions and run along X beside the loops. Clamp screws run
along Y, perpendicular to the draw screws.

There is no printed interlock and no rear tool well. The screws link the
ends; equal adjustment of both sides keeps them parallel. The checked end
gap is 2 to 10 mm, with a default of 6 mm. These are operating limits,
not mechanical stops. Loosening releases tension; it does not positively
push the ends apart.

## Hardware

| Belt | Draw screws | Clamp screws | Nuts |
| --- | --- | --- | --- |
| GT2, 6 or 9 mm wide | 2 x M3x50 socket cap | 2 x M3x16 countersunk | 4 x M3 |
| HTD5M, 15 mm wide | 2 x M3x55 socket cap | 2 x M3x25 countersunk | 4 x M3 |

Use fully threaded draw screws and ordinary M3 hex nuts. A 2.5 mm hex driver
enters from outside along each loop's side. The nut pockets retain their
lower hex flats for anti-rotation. Screw tips are intentionally free to
protrude beyond the receiving lugs as the gap closes.

The existing regular buckles now have full-width solid middles. Their
hardware is M3x16 for GT2 and M4x25 for HTD5M, one set for the shared jaw or
two for independent jaws. Tensioner clamp hardware remains M3 for all belts.

## OOBB primitives and print angles

The production cuts use `screw_countersunk` with its matching nut seat,
`oobb_screw_socket_cap`, `oobb_nut` and `oobb_hole`. The assembly hardware
references use the same positive OOBB primitives. Only drive-recess details
are added to the reference screws; their envelopes come from OOBB.

All production screw and nut cuts set `overhang=True`, including the nut
included by the countersunk screw primitive. OOBB supplies its standard
print-mode overhang geometry. Custom teardrop/gabled reliefs are removed;
nominal shaft holes are round and nut pockets retain their hex profile.
Print-only OOBB features stay excluded from nominal assembly geometry.

The mounts are thick rectangular blocks, 9 mm along the screw axis, joined
to their respective parts over the full available height. The screw-head
mount is integral to the black jaw and moves with it. The nut mount is
integral to the teal base. Neither mount has a flared foot or skirt, and
both sit flat on the bed when their own parts are laid out for printing.
The draw-screw height leaves 5.5 mm beneath its axis in the printed jaw.
The round horizontal holes and standard pockets include downward-facing
surfaces. Their printability follows the OOBB features and the slicer's
bridge/support handling, rather than a custom 45-degree roof. Inspect the
sliced holes before printing; actual quality depends on printer and material.

Each printed part uses one colour: teal bases and their integral guides,
black jaws. Purchased fasteners retain metallic appearances in the renders.

## Printing and assembly

1. Print `3dpr.stl` for the complete four-piece set, or print
   `one_end_print.stl` twice. Each single-end kit contains one base and jaw.
   Use the supplied flat orientation. Nominal assembly STLs are reference
   views; use the printer-compensated print files for fabrication.
2. Check socket-head rotation and nut capture in each side lug. Check that
   the transverse clamp nuts fit and that both loose jaws slide on the base.
3. Install one nut in each end's side nut pocket. Rotate one complete end
   180 degrees in XY. Start the two opposing draw screws and set both side
   gaps to 10 mm. Keep the ends parallel; do not load a single screw first.
4. Loop one belt around each elongated guide, teeth inward, meshing the
   return tail with its incoming strand. Fit the jaws and transverse nuts,
   set coarse belt length, then secure the countersunk clamp screws.
5. Tighten the draw screws alternately in equal small increments. Each M3
   coarse screw advances 0.5 mm per turn; reducing the gap by 8 mm requires
   16 turns of EACH screw. Turning one screw alone will skew the assembly.
   Stop at the required tension and keep both gaps within 2 to 10 mm.

Leave the draw screws loose while setting the belt clamps. Closing a jaw
moves its integral head mount sideways by up to 0.5 mm. The print-mode bore
clearance accommodates the resulting small draw-screw angle; the model
checks tilted fasteners with 0.1 mm axial seating allowance for head/nut
rocking. Recheck this movement and seating on the actual print before loading.

At maximum gap both screws retain full engagement through the 3 mm pocket
allowance with at least 1 mm additional thread beyond it. At minimum gap,
the exposed tips have unobstructed clearance outside the belt channels.
The 90-degree clamp/draw arrangement is also separated spatially to avoid
crossing hardware. The populated dimensions select practical screw lengths.

## Validation

The automated checks export the actual OOBB geometry and inspect:

- Four watertight solids, all printed faces at Z=0, and identical bodies
  and jaws after a 180-degree rotation.
- No plastic crossing the gap: no tongues, keys, overlaps or interlocks.
- Two draw axes perpendicular to the clamp axes, positioned beside the loops.
- Gaps 2, 4, 6, 8 and 10 mm for all three belt sizes, with unchanged solid
  volume, correct length change, full nut engagement and open shaft paths.
- No positive-volume belt or OOBB hardware interference with the plastic,
  plus straight driver access from both sides.
- A nominal nut fits the print-mode pocket but cannot rotate 30 degrees
  inside it with the standard OOBB overhang features.
- Standard round bores retain material where the former custom teardrop
  reliefs removed it; screw/nut calls explicitly enable OOBB overhangs.
- Head mounts belong to the jaws, nut mounts belong to the bases, and their
  outside walls remain straight from bottom to top without flared feet.
- Fully closed jaws clear the bases and tilted draw fasteners at both ends
  of the adjustment range, using the OOBB print-mode clearances.
- Regular buckles have material across their full middle width.
- Single-end, exploded, section, base-only and jaw-only layouts.
- OOBB fastener primitive usage in production and reference generation.

The full pulley regression suite runs alongside these tests. Passing these
checks establishes geometry, not a physical working load.

## Physical fit and load trial

No physical print, torque, creep or pull-test result is available yet.
Record belt make, print material, layer height, perimeter count and infill.
Check nut capture, head rotation, both jaws and the complete adjustment
range before fitting belts. Confirm the standard OOBB holes and pockets print cleanly.

Mark belt entry positions and increase measured tension gradually. Watch
for slip, skew, lug bending, nut rotation and cracking. Hold intended service
preload for 1 hour and 24 hours, checking creep and belt backing damage.
Repeat at the intended service temperature and cycle representative prints
to establish an appropriate margin. Stop at the first slip or damage.

This is a stationary belt termination, not a splice that circulates around
pulleys. Static guide radii are prototype allowances, not approved bend
limits for every belt construction. Check fastener retention under the
vibration conditions of the intended installation.

## Research background

The earlier design research remains applicable to the screw mechanism:
[Jakob turnbuckles](https://jakob.co.uk/product/stainless-steel-turnbuckle-right-handleft-hand-thread/)
use opposite thread hands; these end modules instead use ordinary right-hand
screws against captive nuts. [Prusa belt adjustment guidance](https://help.prusa3d.com/article/adjusting-belt-tension-mk4-s-mk3-9-s-mk3-5-s-mk3-s_112380)
separates fine screw adjustment from coarse belt positioning.
[NBK's M3 data](https://www.nbk1560.com/en-US/products/specialscrew/nedzicom/socketheadcapscrew/SLH/SLH-M3/?SelectedLanguage=en-US)
confirms the 0.5 mm pitch. These sources informed the mechanism; they do
not validate the strength of this printed design.

## Regeneration and extension

The option follows populate -> working_oomp -> working_scad drawing function
-> installed OOBB primitive. `style="draw_tensioner"` selects the pair and
`adjustment_gap=6` is the default. Layouts `end_print` / `end_assembled`
return one end. Profiles use `BELT_PROFILES` or complete `belt_dimensions`
overrides, with M3 hardware retained for this connector style.
