# Timing belt buckles and matching end tensioners

`fold_back` and `fold_back_independent` have solid, full-width middles with
straight sides between the rounded loop chambers. The former has one shared
jaw; the latter has one jaw and countersunk screw for each belt.

`draw_tensioner` uses two identical end bodies and two identical jaws. Each
end has an M3 socket-head seat in its jaw and an M3 nut pocket in its base,
at opposite sides of the loop. Rotate the matching end 180 degrees in XY. Two opposing draw screws
run along X, with the belt clamp screws along Y at 90 degrees. There is no
printed interlock and no rear tool well. See [assembly and validation](DRAW_TENSIONER.md).

All screw and nut cutouts use OOBB primitives with `overhang=True`.
There are no custom teardrop or gabled relief cuts. The library supplies its
standard print-mode overhang geometry; nominal reference holes remain round
and nut pockets hexagonal. The draw-screw mounts are full-height rectangular
blocks without flared feet. Each head mount is integral to the black jaw;
each nut mount is integral to the teal base. Both print on their part's flat face.
The lower hex flats remain to capture each nut against rotation.

The base is 3 mm thick, with 1 mm recessed loop tracks and 2 mm floors.
The guides extend an extra belt pitch: 2 mm GT2 / 5 mm HTD5M. The outer taper
extends equally, preserving channel clearance and five pitches of clamping
length. Integral guides share the single teal material of their bases;
whole jaws are black. No multicolour printing is required.

`depth` / `belt_width` is nominal belt width along Z. Folds lie in XY.
`BELT_PROFILES` holds pitch, thickness, tooth height and static bend allowance.
Add a registry entry or supply all four values in `belt_dimensions`.
`guide_extension`, `overlap_teeth`, `compression_gap`, `width_clearance`,
`base_thickness`, `channel_depth` and `slide_clearance` tune the geometry.
Prototype bend allowances do not establish minimum bend limits for all belts.

Layouts: `print`, `assembled`, `exploded`, `lower`, `upper`, `section`.
The tensioner also supports `end_print` and `end_assembled` for one end.
`adjustment_gap` ranges from 2 to 10 mm and defaults to 6 mm. `pos` / `rot`
transform the complete layout. Jaw print faces lie at Z=0.

Use the standard populate -> working_oomp -> working_scad drawing function
-> installed primitive route. `action_belt_coupler_layouts.py` produces
single-end files and schematic assembly references. `render_belt_couplers.py`
renders the current meshes using the OOBB house palette and studio lighting.
The library install command copies these sources to the active OOBB checkout.
