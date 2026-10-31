# Gridfinity tray with quarter increments

OOBB shape: `gridfinity_tray_quarter_increment`.

Uses the existing Gridfinity Extended tray and pad profiles, with a separate
bottom mask that splits fractional feet. The original `gridfinity_tray_raw`
component and its vendored sources are unchanged.

Width is X, height is Y, and depth is Z, all in Gridfinity units (42/42/7 mm).
Both `gridfinity_width`/`gridfinity_height`/`gridfinity_depth` and the shorter
`width`/`height`/`depth` aliases work. Position and rotation work as usual.

| Tray footprint | Bottom feet |
| --- | --- |
| 0.75 × 1 | 0.5 × 1 + 0.25 × 1 |
| 1 × 0.75 | 1 × 0.5 + 1 × 0.25 |
| 0.75 × 0.5 | 0.5 × 0.5 + 0.25 × 0.5 |
| 0.5 × 0.25 | 0.5 × 0.25 |
| 1.25 × 1 | 1 × 1 + 0.25 × 1 |
| 1.75 × 1 | 1 × 1 + 0.5 × 1 + 0.25 × 1 |

Only one axis may end in .25 or .75. The other must be a multiple of 0.5.
Dimensions must be positive multiples of 0.25; unsupported dimensions raise an
error. Whole-unit feet come first, then any half-unit and quarter-unit remainder.
The `near` alignment places the remainder at the far end; `far` mirrors it.
Center alignment is unsupported. `sub_pitch` and `flat_base` are retained in the
common parameter signature but the component controls them to preserve this
foot layout and the standard floor height.

The interior now follows the bottom feet by default, like the default tray's
efficient floor. Each whole/half/quarter foot has its own recess, with material
left across the seams to keep the tray closed. The nominal 0.7 mm floor has an
additional 0.01 mm boolean clearance. Use `efficient_floor="off"` to retain a
flat interior floor.

```python
oobb.append_full(
    thing,
    shape="gridfinity_tray_quarter_increment",
    gridfinity_width=0.75,
    gridfinity_height=1,
    gridfinity_depth=18 / 7,
    wall_thickness=1.25,
    lip_style="none",
)
```

Validation: `python -m pytest -q tests/test_gridfinity_tray_quarter_increment.py`.
The geometry tests require OpenSCAD with the Manifold backend, trimesh and numpy.
They check individual foot dimensions, one connected watertight mesh, closed
foot bottoms, and the depth of the recesses, with both efficient and flat floors.
Physical fit still requires a print check.
