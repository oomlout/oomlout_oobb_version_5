# OOBB GT2 and HTD5M timing pulleys

`oobb.oobb_easy(shape="oobb_timing_pulley", number_of_teeth=60, depth=6)`
returns a printable pair of clamshell halves. `layout="assembled"` returns the
assembled model. `lower`, `upper`, `exploded`, and `section` support inspection.
The origin is the belt centre; `split_z` records the mating plane. Both split mating faces rest on Z=0 in
the print layout; the lower half is flipped about X. Whole-part `rot` and `pos`
are applied after the layout.

Styles: `basic`, `idler_bearing_606`, `mechanical_coupling_underneath`, and
`mechanical_coupling_recessed`. Small GT2 basic pulleys below 40 teeth are one piece.
Invalid hardware combinations raise `ValueError` before drawing.

Set `belt_profile="htd5m"` for 5 mm pitch HTD teeth; the default `"gt2"`
retains the existing 2 mm pitch geometry. For example:

```python
oobb.oobb_easy(
    shape="oobb_timing_pulley",
    belt_profile="htd5m",
    number_of_teeth=24,
    depth=15,
    style="basic",
    layout="print",
)
```

The HTD5M profile uses the HTD_5mm polygon from the bundled legacy tooth
library, with a pitch-radius offset of 0.5715 mm. Its root keepout follows
the groove placement and fit allowances. Basic HTD5M pulleys split only when
their root circle has room for the shaft and joining hardware. Additional
tooth counts and belt widths need only new populate dictionaries.
`additional_tooth_width` (0–0.5 mm) and `additional_tooth_depth` (0–0.3 mm)
adjust groove fit independently of the nominal pitch.

The primitive uses `pulley_gt2` or `pulley_htd5m` for the teeth, `oobb_cylinder` for flanges and
pockets, `oobb_hole` for bores, and `screw_countersunk` with `nut=True` and
`overhang=True` for joining hardware. Coupler dimensions are provided in a
`coupler` dictionary; the part repository copies these from the OOMP flange CSV.
606 dimensions come from the OOBB bearing CSV (6 x 17 x 6 mm).

`dimensions(**kwargs)` returns validated dimensions, hardware positions,
clearances, assembled bounds, and print spacing. Use the same function for
catalogue metadata and geometry checks.

OOBB mounting holes are enabled by default: M6 at centred 15 mm grid positions,
falling back to M3 at the same position when M6 cannot fit, and M3 at intervening
7.5 mm positions. Every fallback repeats all clearance checks, including the
M3-specific Allen-key exclusion. The central bore is retained. A hole is added
only when its full mode-aware envelope clears the tooth roots, centre pocket or
metal flange, joining and coupling hardware. M3 holes also clear the single +X
Allen-key window; M6 holes may cross it. The minimum
web is `oobb_hole_minimum_web=0.3` mm. `joining_rotation=45` offsets basic and
idler joining fasteners from the grid axes. Recessed couplers default to
`joining_rotation=0`, placing the separate joining screws on the X/Y axes to
preserve eight M3 positions at (+/-15, +/-7.5) and (+/-7.5, +/-15).
The nearby axial M6 positions are excluded where they overlap those screws.
Set `oobb_holes=False` to omit the
additional pattern. `dimensions()` records accepted positions and exclusions.

The 60-tooth GT2 basic and 606 idler pulleys gain four M3 holes at
(-15, 0), (15, 0), (0, -15), and (0, 15) mm. Their print-adjusted diameter is
3.6 mm and the conservative tooth-root wall is 1.145 mm. The 144-tooth GT2
pulleys also gain four M3 holes at (+/-30, +/-30) mm, with a 0.456 mm root wall,
above the existing 0.3 mm minimum. All existing M6 holes remain M6.

The populated coupling style has the same belt-width-based body thickness as
basic: 6.5/9.5 mm channels for 6/9 mm belts, plus two 1 mm flanges. The 10.4 mm
central through hole clears the metal barrel. Four diagonal screws mount the
coupler. Four additional countersunk screws outside the flange join the halves
when the flange pocket reaches the split or leaves less than `minimum_web`
below it. Deeper pulleys share the coupler screws when that lower roof is thick
enough to clamp both halves.
The joining screw on +X has its countersunk head recessed to the keyway floor,
with a straight access well from the top, keeping the Allen-key path clear
after assembly. The other joining screws retain alternating head directions.
Nuts sit below the metal flange, with their bottom faces at the pulley bottom.

`coupler_grub_screw_from_flange=5` places the grub screw halfway along the
10 mm barrel. The flange is raised by its 2 mm thickness plus the 3 mm M3 nut
depth, into a 5 mm underside recess. The barrel projects above the pulley.
For the 6/9 mm belts, the split follows the flange seating face: Z=+0.75/-0.75
mm respectively. The lower half is 5 mm deep; the upper is 3.5/6.5 mm deep.
The complete flange seats flat against the upper mating face, with its shoulder
on the print bed. Deeper pulleys keep the central split when enough material
remains above the flange for shared mounting screws. Both mating faces remain
on the print bed.

There is one cylindrical 4 mm diameter grub-screw clearance on +X, cut with
`oobb_cylinder` for every recessed flange version. Its circular section is
retained when it opens through the top face. For 6/9 mm belts, its lowest point
is at Z=3.75/2.25 mm respectively. M6 grid holes pass through the keyway. The four
coupler screws retain their countersunk seats above the recessed flange.

`coupler_reference(**kwargs)` provides the measured metal flange/barrel/bore/
mount geometry and the specified mid-barrel grub screws for review layouts.
Production `action()` never includes that non-printing metal reference.
