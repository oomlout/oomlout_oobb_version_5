# oobb_wire

Reusable wire-holder cutouts migrated from `oomlout_oobb_electronic_version_5`.
Select the connector with `wire_type` in `kwargs`: `basic` (default), `power`,
`motor`, `motor_stepper`, or `i2c`. `type` remains the OOBB boolean polarity.

```python
import oobb

# The host plate belongs to your project.
oobb.append_full(thing, shape="oobb_plate", type="positive",
                 width=3, height=3, depth=4, pos=[0, 0, 0])
oobb.append_full(thing, shape="oobb_wire", type="negative",
                 wire_type="motor", depth=4, height=3,
                 polarizing_pin=True, pos=[0, 0, 0])
```

The default 3x3 host footprint is 44x44 mm. The local origin is the centre of
its bottom face; the exit faces negative Y, at Y=-22 mm. `pos` places that origin
and `rot=[rx, ry, rz]` rotates the entire feature before placement. `front_y`
overrides the local front edge in millimetres for a different host shape.

The narrow entry goes through the host, with 1 mm overshoot above and below.
The run behind the header pocket is at least 14 mm long for the Dupont housing.
Short runs extend toward the entry without moving the header pocket or exit;
connector styles and larger hosts with longer runs retain their clearance.
The housing run, header pocket and front exit are 2.8 mm deep from the top surface, leaving a
1.2 mm floor in a 4 mm plate. Hardware dimensions retain the original 2.54 mm
pitch and 0.54 mm header clearance; they do not scale with plate dimensions.

`polarizing_pin=True` includes the original semicircular pin-clearance notch
beside the exit on `basic`, `power`, and `i2c`. Set it to `False` to remove that
notch. The offset keyed exit remains; motor styles have no such notch.

| kwarg | Default | Meaning |
| --- | --- | --- |
| `wire_type` | `"basic"` | Connector style |
| `polarizing_pin` | `True` | Include the polarizing pin clearance notch |
| `plate` | `False` | Include a plain OOBB plate, without mounting holes |
| `width`, `height` | `3`, `3` | OOBB units; height locates the front edge, width is for the optional plate |
| `depth` | `4` | Host thickness in mm |
| `cutout_depth` | `2.8` | Housing run / header pocket / exit depth below the top in mm |
| `front_y` | derived from height | Front edge in local mm |
| `pos`, `rot` | `[0, 0, 0]` | Whole-feature placement / rotation |
| `type` | `"negative"` | Boolean polarity; defaults to `"positive"` with `plate=True` |
| `inclusion`, `m` | `"all"`, `""` | Standard render-mode filter / OpenSCAD modifier |

For an optional plain plate, use:

```python
oobb.append_full(thing, shape="oobb_wire", plate=True, wire_type="power")
```

This returns a grouped plate-minus-void, so it can be positioned, rotated, or
subtracted as one object. The electronic project's six M6 mounting holes and
six M3 pin holes stay in that project's `working_scad.get_wire`.

Run `python -m unittest tests.test_oobb_wire_component -v` from the library root
for regression checks of the clearance dimensions and Dupont housing fit. Run this
component's `working.py` for previews of all five styles.
